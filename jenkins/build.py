#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'web'

from time import sleep
from jenkinsapi.jenkins import Jenkins

jenkins_url = 'http://172.16.200.111:8090'
job_name = '测试-测试'
server = Jenkins(jenkins_url, username='dbn_admin', password='afddd3031a2663e2f4cd56fa5bd4a022')


last_buildnumber = job.get_last_completed_buildnumber()
current_buildnumber = last_buildnumber + 1


def build(job_name)
    server.build_job(job_name)
    job = server.get_job(job_name)
    # check if buid started
    this_build_id = job.get_last_buildnumber() + 1
    while job.get_last_buildnumber() != this_build_id:
        job = server.get_job(job_name)
        print("job:{0} id{1} not start yet".format(job_name, this_build_id))
        sleep(3)

    this_build = job.get_build(this_build_id)

    # check wether build is running
    while not this_build.is_good():
        sleep(3)
        print("job:{0} id:{1} is running".format(job_name, this_build_id))

    # check build result
    print(this_build.get_status())
