import java.time.format.DateTimeFormatter
import java.time.LocalDate

def compose_topurl = 'https://odcs.stream.rdu2.redhat.com/composes'
def compose_types = ['production', 'development'] as Set
def compose_release = 'CentOS-Stream'

pipeline {
    agent {
        label '!windows'
    }

    stages {
        stage('Generate compose report') {
            steps {
                script {
                    sh "./scripts/last_good/report.py"
                }
            }
        }
    }
}
