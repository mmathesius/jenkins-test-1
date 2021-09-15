def failure_days_to_notify = 0
def failure_email_sender = "Compose Alert <compose-alert@centos.org>"
def failure_email_recipient = "mmathesi@redhat.com"

def composeattrs = null
def buildstatus = 'UNKNOWN'

import java.time.format.DateTimeFormatter
import java.time.LocalDate

pipeline {
    agent {
        label '!windows'
    }

    stages {
        stage('Submit Compose') {
            steps {
                sh 'printenv'
            }
        }

        stage('Wait for Compose to finish') {
            steps {
                // timeout(time: 120, unit: 'MINUTES') { //120 minutes
                timeout(time: 90, unit: 'SECONDS') {
                    script {
                        buildstatus = 'UNKNOWN'
                        Exception caughtException = null

                        // if an error occurs, abort this stage without failing the build
                        catchError(buildResult: null, stageResult: 'ABORTED') {
                            try {
                                while( true ) {
                                    sleep 60 // seconds
                                    // sh "curl --negotiate -u : -o response.json https://odcs.stream.rdu2.redhat.com/api/1/composes/$composeid"

                                    composeattrs = readJSON file: 'response.json'

                                    if (composeattrs['state'] == 2) { //done
                                        buildstatus = 'SUCCESS'
                                        return
                                    } else if (composeattrs['state'] == 4) { //failed
                                        buildstatus = 'FAIL'
                                        return
                                    }
                                }
                            } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
                                buildstatus = 'TIMEOUT'
                                error "Caught ${e.toString()}"
                            } catch (Throwable e) {
                                caughtException = e
                            }
                        } // catchError()

                        // if an unexpected exception occurred, go ahead and fail the build
                        if (caughtException) {
                            error caughtException.message
                        }
                    }
                } // timeout()
            }
        } // stage()

        stage('Report Compose Result') {
            steps {
                script {
                    def buildname = "unknown-build"
                    if (composeattrs) {
                        buildname = composeattrs['pungi_compose_id']
                        currentBuild.displayName = "$buildname"
                    }

                    echo "Build $buildname status: $buildstatus"

                    if (buildstatus != 'SUCCESS') {
                        // track down details for latest successful compose
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
                            def failure_subject = "Development compose $buildname pipeline has not succeeded for $failed_days days"
                            def failure_message = """Greetings.

Jenkins development compose build $buildname status is $buildstatus.
The pipeline has not succeeded for $failed_days days.

Job URL: ${BUILD_URL}"""
                            emailext to: failure_email_recipient,
                                from: failure_email_sender,
                                subject: failure_subject,
                                body: failure_message
                        }
                        error "Compose Status $buildstatus"
                    }
                }
            }
        }
    }
}
