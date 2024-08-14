#!/bin/bash


echo 'Getting TOMCAT_HOME from SSM'



mv /tmp/webapp.war /opt/jetty/webapps/

# Stop Tomcat


# Wait for Tomcat to fully start (adjust the sleep duration based on your application's startup time)
sleep 60

# Start Tomcat
/opt/jetty/bin/jetty.sh stop
/opt/jetty/bin/jetty.sh start

# Wait for Tomcat to fully start (adjust the sleep duration based on your application's startup time)
sleep 60



# Additional commands or configurations after Tomcat has started can be added here
# For example, you might want to tail the catalina.out log file for debugging:
# tail -f $TOMCAT_HOME/logs/catalina.out
