import java.time.format.DateTimeFormatter
import java.time.LocalDate

def compose_topurl = 'https://odcs.stream.rdu2.redhat.com/composes'
def compose_types = ['production', 'development'] as Set
def compose_release = 'CentOS-Stream'

pipeline {
    agent {
        label '!windows'
    }

    // environment {
    //     VARIABLE     = 'value'
    // }

    stages {
        stage('Setup') {
            steps {
                sh 'printenv'
            }
        }

        stage('Generate compose report') {
            steps {
                script {
                    today_edays = LocalDate.now().toEpochDay()

                    for (compose_type in compose_types) {
                        echo ">> $compose_type REPORT GOES HERE <<<"
                        latest_composeurl = "$compose_topurl/$compose_type/latest-$compose_release"
                        composeinfo_url = "$latest_composeurl/compose/metadata/composeinfo.json"
                        response = httpRequest url: composeinfo_url, outputFile: "composeinfo.json", ignoreSslErrors: true
                        latest_composeinfo = readJSON file: "composeinfo.json"
                        latest_composeid = latest_composeinfo["payload"]["compose"]["id"]
                        latest_composedate = latest_composeinfo["payload"]["compose"]["date"]

                        echo "Latest successful $compose_type compose $latest_composeid date: $latest_composedate"

                        compose_edays = LocalDate.parse(latest_composedate, DateTimeFormatter.ofPattern("yyyyMMdd")).toEpochDay()
                        failed_days = today_edays - compose_edays

                        echo "Latest successful $compose_type compose $latest_composeid was $failed_days days ago."
                    }
                }
            }
        }
    }
}
