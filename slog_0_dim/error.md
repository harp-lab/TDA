### System information
- Docker version
```
docker --version
Docker version 26.1.3 (Ubuntu 23.10)
docker version
Docker version 24 (Ubuntu 22.04)
```
- OS
```
Ubuntu 23.10
```

### Error in prebuilt image
Terminal freezes on docker run command
```
docker pull stargazermiao/slog
docker run --rm -it -v $(pwd):/workspace stargazermiao/slog
```

### Error in building from source
```
➜  slog_docker git clone https://github.com/harp-lab/slog.git
Cloning into 'slog'...
remote: Enumerating objects: 6024, done.
remote: Counting objects: 100% (6024/6024), done.
remote: Compressing objects: 100% (1857/1857), done.
remote: Total 6024 (delta 3969), reused 5882 (delta 3902), pack-reused 0
Receiving objects: 100% (6024/6024), 94.43 MiB | 20.34 MiB/s, done.
Resolving deltas: 100% (3969/3969), done.
➜  slog_docker cd slog
➜  slog git:(master) docker build -t slog .
[+] Building 175.5s (8/16)                                       docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 1.57kB                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:jammy            0.9s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 132B                                          0.0s
 => [ 1/12] FROM docker.io/library/ubuntu:jammy@sha256:19478ce7fc2ffbce89  1.9s
 => => resolve docker.io/library/ubuntu:jammy@sha256:19478ce7fc2ffbce89df  0.0s
 => => sha256:7646c8da332499ae416b15479ce832db32e39a501 29.53MB / 29.53MB  0.8s
 => => sha256:19478ce7fc2ffbce89df29fea5725a8d12e57de52eb 1.13kB / 1.13kB  0.0s
 => => sha256:94db6b944510db19c0ff5eb13281cf166abfe6f9e01a6f8 424B / 424B  0.0s
 => => sha256:67c845845b7de8024a1ad9f6e7fd08964502a0b423a 2.30kB / 2.30kB  0.0s
 => => extracting sha256:7646c8da332499ae416b15479ce832db32e39a501c662e24  1.0s
 => [internal] load build context                                          1.0s
 => => transferring context: 183.20MB                                      1.0s
 => [ 2/12] RUN apt-get update && apt-get install -y wget gnupg software  35.4s
 => [ 3/12] RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | ap  0.7s 
 => ERROR [ 4/12] RUN add-apt-repository ppa:plt/racket                  136.6s 
------                                                                          
 > [ 4/12] RUN add-apt-repository ppa:plt/racket:                               
136.5 Traceback (most recent call last):                                        
136.5   File "/usr/bin/add-apt-repository", line 364, in <module>               
136.5     sys.exit(0 if addaptrepo.main() else 1)                               
136.5   File "/usr/bin/add-apt-repository", line 347, in main
136.5     shortcut = handler(source, **shortcut_params)
136.5   File "/usr/lib/python3/dist-packages/softwareproperties/shortcuts.py", line 40, in shortcut_handler
136.5     return handler(shortcut, **kwargs)
136.5   File "/usr/lib/python3/dist-packages/softwareproperties/ppa.py", line 82, in __init__
136.5     if self.lpppa.publish_debug_symbols:
136.5   File "/usr/lib/python3/dist-packages/softwareproperties/ppa.py", line 120, in lpppa
136.5     self._lpppa = self.lpteam.getPPAByName(name=self.ppaname)
136.5   File "/usr/lib/python3/dist-packages/softwareproperties/ppa.py", line 107, in lpteam
136.5     self._lpteam = self.lp.people(self.teamname)
136.5   File "/usr/lib/python3/dist-packages/softwareproperties/ppa.py", line 98, in lp
136.5     self._lp = login_func("%s.%s" % (self.__module__, self.__class__.__name__),
136.5   File "/usr/lib/python3/dist-packages/launchpadlib/launchpad.py", line 494, in login_anonymously
136.5     return cls(
136.5   File "/usr/lib/python3/dist-packages/launchpadlib/launchpad.py", line 230, in __init__
136.5     super(Launchpad, self).__init__(
136.5   File "/usr/lib/python3/dist-packages/lazr/restfulclient/resource.py", line 472, in __init__
136.5     self._wadl = self._browser.get_wadl_application(self._root_uri)
136.5   File "/usr/lib/python3/dist-packages/lazr/restfulclient/_browser.py", line 447, in get_wadl_application
136.5     response, content = self._request(url, media_type=wadl_type)
136.5   File "/usr/lib/python3/dist-packages/lazr/restfulclient/_browser.py", line 389, in _request
136.5     response, content = self._request_and_retry(
136.5   File "/usr/lib/python3/dist-packages/lazr/restfulclient/_browser.py", line 359, in _request_and_retry
136.5     response, content = self._connection.request(
136.5   File "/usr/lib/python3/dist-packages/httplib2/__init__.py", line 1725, in request
136.5     (response, content) = self._request(
136.5   File "/usr/lib/python3/dist-packages/launchpadlib/launchpad.py", line 144, in _request
136.5     response, content = super(LaunchpadOAuthAwareHttp, self)._request(
136.5   File "/usr/lib/python3/dist-packages/lazr/restfulclient/_browser.py", line 184, in _request
136.5     return super(RestfulHttp, self)._request(
136.5   File "/usr/lib/python3/dist-packages/httplib2/__init__.py", line 1441, in _request
136.5     (response, content) = self._conn_request(conn, request_uri, method, body, headers)
136.5   File "/usr/lib/python3/dist-packages/httplib2/__init__.py", line 1363, in _conn_request
136.5     conn.connect()
136.5   File "/usr/lib/python3/dist-packages/httplib2/__init__.py", line 1153, in connect
136.5     sock.connect((self.host, self.port))
136.5 TimeoutError: [Errno 110] Connection timed out
------
Dockerfile:6
--------------------
   4 |     
   5 |     RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
   6 | >>> RUN add-apt-repository ppa:plt/racket
   7 |     RUN apt-get update && apt-get install -y clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 libc++abi-dev \
   8 |                 libc++abi1 libclang-dev libclang1 liblldb-dev libomp-dev libomp5 lld lldb \
--------------------
ERROR: failed to solve: process "/bin/sh -c add-apt-repository ppa:plt/racket" did not complete successfully: exit code: 1

```
