pipeline {
    agent {
        label 'compose'
    }

    environment {
        VARIABLE     = 'value'
    }

    stages {
        stage('Setup') {
            steps {
                sh 'printenv'
            }
        }

        stage('Generate compose report') {
            steps {
                script {
                }
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

                        echo "Latest successful compose was ${failed_days} days ago."

                        error 'Compose Failed'
                    }
                }
            }
        }
    }
}
