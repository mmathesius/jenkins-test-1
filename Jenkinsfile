def failure_days_to_notify = 0
def failure_email_sender = "Compose Alert <compose-alert@centos.org>"
def failure_email_recipient = "mmathesi@redhat.com"

import java.time.format.DateTimeFormatter
import java.time.LocalDate

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

                        def url = "$toplevel_url/../$compose_type/latest-CentOS-Stream/compose/metadata/composeinfo.json"
                        def response = httpRequest url: url, outputFile: "composeinfo.json", ignoreSslErrors: true
                        def latest_composeinfo = readJSON file: "composeinfo.json"
                        def latest_composedate = latest_composeinfo["payload"]["compose"]["date"]

                        echo "Latest successful compose date: ${latest_composedate}"

                        def compose_edays = LocalDate.parse(latest_composedate, DateTimeFormatter.ofPattern("yyyyMMdd")).toEpochDay()
                        def today_edays = LocalDate.now().toEpochDay()
                        def failed_days = today_edays - compose_edays

                        echo "Latest successful compose was ${failed_days} days ago. Notification threshold is ${failure_days_to_notify} days."

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
