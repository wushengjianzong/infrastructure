#!python

import os
import sys
import subprocess

kube_pki_path = '/etc/kubernetes/pki'

if __name__ == '__main__':
    server: str = sys.argv[1]
    cluster: str = sys.argv[2]
    user: str = sys.argv[3]

    cwd: str = os.getcwd()

    subprocess.call(f"ssh root@{server} openssl genrsa -out {kube_pki_path}/{user}.key 2048", shell=True)
    subprocess.call(f"ssh root@{server} openssl req -new -key {kube_pki_path}/{user}.key -out {kube_pki_path}/{user}.csr -subj /CN={user}/O=cluster-admin", shell=True)
    subprocess.call(f"ssh root@{server} openssl x509 -req -in {kube_pki_path}/{user}.csr -CA {kube_pki_path}/ca.crt -CAkey {kube_pki_path}/ca.key -CAcreateserial -out {kube_pki_path}/{user}.crt -days 3650", shell=True)
    subprocess.call(f"ssh root@{server} kubectl create clusterrolebinding {user} --clusterrole=cluster-admin --user {user} --group cluster-admin", shell=True)

    subprocess.call(f"scp root@{server}:{kube_pki_path}/ca.crt {cwd}", shell=True)
    subprocess.call(f"scp root@{server}:{kube_pki_path}/{user}.key {cwd}", shell=True)
    subprocess.call(f"scp root@{server}:{kube_pki_path}/{user}.crt {cwd}", shell=True)

    subprocess.call(f"kubectl config set-cluster {cluster} --certificate-authority ca.crt --server https://{server}:6443 --embed-certs", shell=True)
    subprocess.call(f"kubectl config set-credentials {user} --client-certificate {user}.crt --client-key {user}.key --embed-certs", shell=True)
    subprocess.call(f"kubectl config set-context {user}@{cluster} --user {user} --cluster {cluster}", shell=True)
    subprocess.call(f"rm ca.* {user}.*", shell=True)

