
##
1.⁠ ⁠get the data by running
⁠ wget -c --retry-connrefused --tries=0 --timeout=50 http://aliopentrace.oss-cn-beijing.aliyuncs.com/v2017Traces/alibaba-trace-2017.tar.gz ⁠ 
##
2.⁠ ⁠unzip by ⁠ tar -xvf <file.tar.gz> ⁠
##
3.⁠ ⁠⁠run the code in data_preprocess.py by setting the directories by opening a tmux session to keep it in background.
##
4. conda deactivate, conda activate in case python version gives error
##
5. create out folder
##
6. execute command `python3 run_detect.py --data_path ./alibabatimeseries2017f --jobid 9098`
