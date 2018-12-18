import speech_recognition as sr
from os import path

# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "my-speech2text",
  "private_key_id": "5c0f2d54a2a29bf0a4a1e7385e9d9edb72f14b8f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDa+H8mSz+qRvt2\n29cM2/Aw60z1gXUJS72nYHsPUuTIS4veqUXXLws7Xvv2iWFwyUHoSQLErOs6KEfY\nJB/fRcB7p0U+HAqcHemjKo3zqu1RJoN80Wvph1gxSOzCc4T7K3E5/WmSO/A8bfWL\ntdaQDs6Eo/1UI3oG3r3P2A36fZmUM/CS/3/+XMkObSmEaejqyb+ABj2CAZ3ARMu3\n6Cjn6V5FxsuLqwTx1QjhDMli9JSpWgsrc/AM0jgSQSMjDZDj+YM0A/GfGfEKTZYV\nKz8b0NENwi5VfIrxrwnkTve4BuJA/85EgKmaliFOfoHHnS2VvcNJApa77zoIvfkQ\nctaXfixtAgMBAAECggEABx0FfGf7ZHuz1ZOks809S0mJkXwoIiosuhA/TyshNYSG\nwa/8DdaAZehbBRJHcROIqZQdm+gGKDiAxPu/cVBhxWKUtETS72llWqCaRe0qknVO\n1jIzcD2uVsOItXRtQH+TyQ97a324+y2TSXuZwcpJWTO+mgog/7IitmrNYXLNF2xd\nJVFlXCmkirrZD+WT5qykwWz+AMdYC4/pQHGGkebnYxrfvFnfjsavd6UuqTlRO9MR\nARyrDVBmVlulBbpu5yyw0NHnMaNBwpv1RatrpqOjJOn31mQ/bQE4WUa41CL5kcnU\n24N761Ni3OQhpyH/aLqoveEKYDqnEzxKhEhXTUglvQKBgQDtHHZWOyYMlI/O0lN3\nrBqdKHOh2XdXsYaC+A5AFyJXU374vUUFdsv9gaSALXGb1f6PzoBWjPPE3ol0SznQ\nKP62Q6WgbRpOpivHD/RsON8/JGascVzzbrxKuaQSTTJ3amzA4amUpx8j7OQsvsmX\n5Il+XUOslUb6I6jRrUzy+8glywKBgQDsahXjO3Uts4j3w+1X189O0vk+vLMOwawH\niM5dR+HtVVSWqDUwlRleTSwghIPCN7mnWd1VrxIToxDbxQOnhrjoadlTS2+ndR7R\nG/ouoCxlPBJtxF5hnJpTIK3E9+Zee0LFjwyJ2e+xO7oC4DnY8Quwtxre75T5Uy6s\n6OBwGU/vpwKBgHeg2Y+ODhdgyOF3OkdxnIfYBecNmemzloLzdfUd9uSKKtCCZZVp\nJ2hChWVqCBywrduOOy/vs3mLMVxsK8H7PO9mV+UFxrURn5qyUQZc9z2bNvYfx97F\n6tfkq4PUUPbwyefSssVeQBbXCRQOOhWZZ0lK8r7bHdFMNnt7bQxWvddbAoGBALgp\ne5tjech8DrpTGdRP/OG+XwKMJD/eho/n9jmcAVbMHfSuW6DYxMY8/57lG25z0l+X\nFV/l3QMHB97q/gnGXMxPiEfmf7fG+JaUYLNpeqvxu7leOtd3EpCm6DaDliULh9w1\nruLDroA1spUC7o0cWKr0OC5qG3aNYdK4Jf2s+iQJAoGBANxE5JeDKxKl1ghD1s9K\n40eapMoDdx9HAdU79/X+d/JPXYuDie02IruHPL0Pqm1ZPhV+2uKSxDHYvpKzSb9r\nIaEIJjTDQdw0FVmGjAvgCRWuxNJxOg4tVl8pDqWB9geQ28dS+7azWEFMm9SROX8n\nckmcuqdT3we2ppPW82zLdm57\n-----END PRIVATE KEY-----\n",
  "client_email": "translate@my-speech2text.iam.gserviceaccount.com",
  "client_id": "114527576364506577489",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/translate%40my-speech2text.iam.gserviceaccount.com"
}"""


def get_project_dir():
    path_array = path.dirname(path.realpath(__file__)).split('/')
    proj_root = "/".join(path_array[:len(path_array) - 1])
    return proj_root

# obtain audio from the microphone
r = sr.Recognizer()

audio_file = path.join(path.realpath(get_project_dir()),
                       "resources",
                       "harvard.wav")
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

try:
    print("Google Cloud Speech thinks you said " +
          r.recognize_google_cloud(
                  audio,
                  credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
