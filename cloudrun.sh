project=$1
tag=$2
path=sample-streamlit-chat
# image build
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=_REPOSITORY=${path},_IMAGE=app,_TAG=${tag} .

# deploy
gcloud run deploy --image asia-northeast1-docker.pkg.dev/${project}/${path}/app:${tag} \
 --platform managed \
 --port 8000 \
 --memory 2Gi \
 --cpu 1 \
 --region asia-northeast1 \
 --max-instances 3 \
 --min-instances 0
