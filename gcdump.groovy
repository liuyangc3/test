/**
 * Created by web on 2015/7/2.
 */
import javax.management.remote.JMXServiceURL
import javax.management.remote.JMXConnectorFactory
import java.lang.management.ManagementFactory
import com.sun.management.HotSpotDiagnosticMXBean

// jmx 连接
urlString = "service:jmx:rmi:///jndi/rmi://172.16.200.105:10053/jmxrmi"
jmxSerciceUrl = new JMXServiceURL(urlString)
map = [:]
map["jmx.remote.credentials"] =  ["controlRole", ""]
connection = JMXConnectorFactory.connect(jmxSerciceUrl, map).getMBeanServerConnection()


// bean
HOTSPOT_BEAN_NAME = "com.sun.management:type=HotSpotDiagnostic"
bean = ManagementFactory.newPlatformMXBeanProxy(connection, HOTSPOT_BEAN_NAME, HotSpotDiagnosticMXBean)


// 设置 JVM 参数
bean.setVMOption('HeapDumpBeforeFullGC', 'true')
bean.setVMOption('HeapDumpAfterFullGC', 'true')

// 参数列表
// http://hg.openjdk.java.net/jdk6/jdk6/hotspot/file/tip/src/share/vm/runtime/globals.hpp
// 参考 http://rednaxelafx.iteye.com/blog/1048958