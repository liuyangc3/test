#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import requests
import argparse
import ansible.playbook
from jenkinsapi.jenkins import Jenkins
from ansible import callbacks
from ansible import utils
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class JenkinsApiWrapper(object):
    def __init__(self, jenkins_url, username=None, token=None):
        self.jenkins_url = jenkins_url
        self.server = Jenkins(jenkins_url, username=username, password=token)

    def get_job_by_name(self, job_name):
        """ job_name 返回 job 实例"""
        if self.server.has_job(job_name):
            # 也可以这样 return self.server[job_name]
            return self.server.get_job(job_name)
        raise NameError('can not find job %s' % job_name)

    def get_job_ip_from_job_name(self, job_name):
        """
         从描述部分取出ip和domain
         job_instance.get_description() 返回 job 的描述
        """
        job_description = self.get_job_by_name(job_name).get_description()
        try:
            m = re.match(r'ip:(.*\d+.\d+.\d+.\d+)', job_description)
            # m.group() = ip:a.b.c.d,x,y,m,n  m.group(1) = a.b.c.d,x,y,m,n
            ip_list = m.group(1)
            if ',' not in m.group(1):
                ip = ip_list
            else:
                ip = m.group(1).split(',')
            # m = re.search(r'.*domain:(.*[^\s])', job_description)
            # domain = m.group(1).split(',')
            return ip
        except AttributeError, e:
            print(e)

    @staticmethod
    def _find_war_url_from_war_page(war_page_url):
        """
        从带有 war下载链接的页面取出 war包下载地址
        """
        url = war_page_url
        html = requests.get(war_page_url).text
        test = re.findall(r'war">(.*)war</a>', html)
        war_name = re.findall(r'war">(.*)war</a>', html)[0]
        # war_size = re.findall(r'class="fileSize">(.*) MB</td>', html)[0] + ' MB'
        war_url = war_page_url + war_name + 'war'
        return war_url

    def get_job_war_url(self, job_name):
        """
        根据 job_name 获取 war 包下载地址

        每个job的配置是个xml文档
        curl user:password@jenkins_url/job/job_name/config.xml

        如果job是由 Maven 构建, config.xml中只有 rootPOM 子节点
        如果是 gradle 或者 ant 构建的, 只有 builders 子节点, 该节点会包含以下子节点:
        hudson.plugins.gradle.Gradle 或者 hudson.tasks.Ant
        """
        # encode('utf-8') 用来保证 即便 description 中有汉字 ET 也能正常解析xml
        config = self.server[job_name].get_config().encode('utf-8')
        root = ET.fromstring(config)
        job_name = urllib.quote(job_name)

        def ant_build_path(_instance, root):
            pass

        def maven_build_path(_instance, root):
            # 如果pom.xml 不在仓库的根路径,需要找到pom文件的父目录
            if ET.iselement(root.find('rootPOM')):
                app_path = root.find('rootPOM').text[:-8]  # maven.text = some_path/pom.xml
                war_page = self.jenkins_url + '/job/' + job_name + '/ws/' + app_path + '/target/'
                return self._find_war_url_from_war_page(war_page)
            war_page = self.jenkins_url + '/job/' + job_name + '/ws/target/'
            return _instance._find_war_url_from_war_page(war_page)

        def gradle_build_path(_instance, root):
            pass

        # 如果是采用 maven 构建的job 的配置文件中应该有 rootModule
        if ET.iselement(root.find('rootModule')):
            return maven_build_path(self, root)

        # 如果是 gradle 或者 ant 构建,builders 元素的子元素会指出类型
        elif ET.iselement(root.find('builders')):
            gradle = root.find('builders').find('hudson.plugins.gradle.Gradle')
            ant = root.find('builders').find('hudson.tasks.Ant')

            if ET.iselement(gradle):
                # 如果build.gradle在仓库跟路径, app_path 是None
                app_path = gradle.find('rootBuildScriptDir').text
                if app_path is None:
                    app_path = ""
                war_page = self.jenkins_url + '/job/' + job_name + '/ws/' + app_path + '/build/libs/'
                return self._find_war_url_from_war_page(war_page)
            if ET.iselement(ant):
                # ant 编译的 war 包如果是正式环境的 会放在 output/prod/目录
                # 测试环境 output/test/目录 这里我就不去读取 build.xml了
                # 直接根据 job name 后缀是否带 测试 和 正式 来写死 war包路径
                # 测试和开发

                # 找 build.xml 和 jenkins调用的 targets
                targets_name = ant.find('targets').text
                buildfile = ant.find('buildFile')

                # 解析 build.xml
                if buildfile:
                    xmlpage = self.jenkins_url + '/job/' + job_name + '/ws/' + buildfile.text
                else:
                    xmlpage = self.jenkins_url + '/job/' + job_name + '/ws/build.xml'

                xml = requests.get(xmlpage).text
                build_xml_root = ET.fromstring(xml)
                targets = build_xml_root.findall('target')
                for target in targets:
                    if target.attrib['name'] == targets_name:
                        dest = target.find('war').attrib['destfile']
                        if '$' in dest:
                            _war = self.parse_build_xml(build_xml_root, dest)
                        else:
                            _war = dest
                        break
                war_url = self.jenkins_url + '/job/' + job_name + '/ws/' + _war

                return war_url

    def parse_build_xml(self, root, str_with_brace):
        """ 解析 str_with_brace 内是否还有 变量 ${}, 如果有则查找 property 替换成对应的值 """

        var_list = re.findall(r'(?<=\${)[\w\.]+(?=})', str_with_brace)
        properties = root.findall('property')

        for v in var_list:
            for _property in properties:
                if 'name' in _property.attrib and _property.attrib['name'] == v:
                    value = _property.attrib['value']
                    if '$' in value:
                        res = self.parse_build_xml(root, value)
                    else:
                        res = value
                    str_with_brace = str_with_brace.replace('${' + v + '}', res)
        return str_with_brace
        


def playbook(_playbook, _dict):
    _stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(_stats, verbose=utils.VERBOSITY)

    return ansible.playbook.PlayBook(
        playbook=_playbook,
        host_list='dynamic_inventory.sh',   # 动态主机
        extra_vars=_dict,
        stats=_stats,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        check=False)
        
def update_deploy_script(_playbook, jenkins, job_name):

    war_url = jenkins.get_job_war_url(job_name)
    ip_list = jenkins.get_job_ip_from_job_name(job_name)

    if ip_list.__class__ is str:
        l = [ip_list]
        ip_list = l

    try:
        host = ';'.join(ip_list)
        _dict = {'url': war_url, 'host': host, 'timer_cmd': ''}
        return playbook(_playbook, _dict).run()
    except TypeError, e:
        raise("没有得到主机ip")
        print(e)

if __name__ == '__main__':
    jenkins = JenkinsApiWrapper('http://172.16.200.84:8080')
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", help="jenkons job name")
    args = parser.parse_args()
    print(update_deploy_script('create_deploy_shell_script.yml', jenkins, args.job_name))
