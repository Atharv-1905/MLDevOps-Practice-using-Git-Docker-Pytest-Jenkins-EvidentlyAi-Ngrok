
pipeline {
    agent any

    stages {
        stage('Pull Code from GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Atharv-1905/MLDevOps-Internal-POE.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      --build-arg PIP_DEFAULT_TIMEOUT=180 \
                      -t student-marks-demo:2.0 .
                '''
            }
        }

        stage('Docker Application Test') {
            steps {
                sh 'docker run --rm student-marks-demo:2.0'
            }
        }

        stage('Docker Pytest') {
            steps {
                sh '''
                    docker run --rm student-marks-demo:2.0 \
                      python -m pytest -v
                '''
            }
        }

        stage('Evidently Monitoring') {
            steps {
                sh '''
                    mkdir -p monitoring/reports

                    docker run --rm \
                      -v "$WORKSPACE/monitoring/reports:/app/monitoring/reports" \
                      student-marks-demo:2.0 \
                      python monitoring/data_drift.py

                    test -f monitoring/reports/drift_report.html
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All CI stages completed!'
            archiveArtifacts(
                artifacts: 'monitoring/reports/drift_report.html',
                fingerprint: true
            )
        }

        failure {
            echo 'FAILURE: Check Console Output for the failed stage.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}
