## Run SLOG using Docker
- Pull Docker image
```shell
docker pull stargazermiao/slog
```
- Run SLOG Docker image and mount current directory:
```shell
docker run --rm -it -v $(pwd):/slog/workspace --entrypoint=bash stargazermiao/slog
```
- Run the transitive closure code:
```
./runslog -R --facts workspace/tc/input/ workspace/tc/src/tc.slog workspace/tc/output/
```
- Run the 0-dim code:
```
./runslog -R --facts workspace/0dim/input/ workspace/0dim/src/cc.slog workspace/0dim/output/
```
- It will open a REPL. To show all the output paths
```shell
dump path
```



### References
- [SLOG docker doc](https://slog-wiki.notion.site/Local-Setup-from-Docker-and-Source-8ba93eab612e450293b289a61435310f)
- [SLOG TC example](https://github.com/harp-lab/slog-lang1/blob/master/doc/TC.md)
- [Comparison of Slog and Soufflé](https://github.com/harp-lab/slog-lang1/blob/master/doc/compare.md)
