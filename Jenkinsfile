def failure_days_to_notify = 2
def failure_email_sender = "merlinm-jenkins-test@redhat.com"
def failure_email_recipient = "mmathesi@redhat.com"

pipeline {
    agent {
        label '!windows'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }

        stage('Report Compose result') {
            steps {
                script {
                    def composeattrs = readJSON file: 'response.json'
                    def buildname = composeattrs['pungi_compose_id']
                    def buildstatus = (composeattrs['state'] == 4) ? 'FAIL' : 'SUCCESS'
                    currentBuild.displayName = "$buildname"

                    echo "Build $buildname status: $buildstatus"

                    if (buildstatus == 'FAIL') {
                        // track down details for last successful compose
                        def toplevel_url = composeattrs['toplevel_url']
                        def compose_type = composeattrs['compose_type']

                        url = "$toplevel_url/../$compose_type/latest-CentOS-Stream/compose/metadata/composeinfo.json"

                        echo "URL with compose details for last successful build of type $compose_type: $url"

                        def response = httpRequest url: url, outputFile: "composeinfo.json", ignoreSslErrors: true
                        echo "URL fetch status: ${response.status}"
                        echo "URL download content:"
                        sh "cat composeinfo.json"

                        // def json = new JsonSlurper().parseText(response.content)
                        // echo "JSON: ${json}"

                        failed_days = 0

                        if (failed_days >= failure_days_to_notify) {
                            def failure_subject = "Development compose $buildname pipeline has been failing for $failed_days days"
                            def failure_message = """Greetings.

Jenkins development compose build $buildname pipeline has been failing for $failed_days days.

Job URL: ${BUILD_URL}"""
                            emailext to: failure_email_recipient,
                                from: failure_email_sender,
                                subject: failure_subject,
                                body: failure_message
                        }
                        error 'Compose Failed'
                    }
                }
            }
        }
    }
}
