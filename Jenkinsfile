pipeline {
  agent any

  environment {
        GIT_NAME = "eea.progressbar"
    }
  
  stages {
       stage('Functional tests') {
      steps {
        parallel(

          "WWW": {
            node(label: 'docker-1.13') {
                script {
                  try {
                  sh '''docker run -i --net=host --name="$BUILD_TAG-plone4" -v /plone/instance/parts -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" plone4test -v -vv -s $GIT_NAME'''
                } finally {
                  sh '''docker rm -v $BUILD_TAG-plone4'''
                  }
                }
            }
          },

          "KGS": {
            node(label: 'docker-1.13') {
               script {
                 try {
                  sh '''docker run -i --net=host --name="$BUILD_TAG-kgs" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" kgs-dev /debug.sh bin/test --test-path /plone/instance/src/$GIT_NAME -v -vv -s $GIT_NAME'''
                } finally {
                  sh '''docker rm -v $BUILD_TAG-kgs'''
                }
               }
            }
          },

          "Plone4": {
            node(label: 'docker-1.13') {
              script {
                try {
                     checkout scm
                     sh '''docker run -p 8080 -d -e ADDONS=eea.progressbar -e DEVELOP=src/eea.progressbar --name=$BUILD_TAG-ft-plone4 eeacms/plone-test:4'''
                     sh '''docker port $BUILD_TAG-ft-plone4 8080/tcp > url.file;docker_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' $BUILD_TAG-ft-plone4); sed -i -e "s/0.0.0.0/${docker_ip}/g" url.file'''
                     sh '''new_url=$(cat url.file);timeout 300  wget --retry-connrefused --tries=60 --waitretry=5 -q http://${new_url}/'''
                     sh '''new_url=$(cat url.file);casperjs test eea/progressbar/ftests/plone4/*.js --url=${new_url} --xunit=ftestsreport.xml'''
                
                }
                finally {
                  sh '''docker stop $BUILD_TAG-ft-plone4'''
                  sh '''docker rm -v $BUILD_TAG-ft-plone4'''
                }
               }
              junit 'ftestsreport.xml'
              archiveArtifacts 'screenshot1.png'

              }

            }
          )
      }
    }
    
  }
}
