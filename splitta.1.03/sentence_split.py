#!/usr/local/bin/python
#coding:utf-8

import sys
import os
import re

input_dir=sys.argv[1]
output_dir=sys.argv[2]
LEN_MIN=int(sys.argv[3])	#设置LEN_MIN,单行长度小于LEN_MIN的排除
if not os.path.exists(input_dir):
	print 'input_file error'
	exit()
if not os.path.exists(output_dir):
	os.mkdir(output_dir)

i=1
#预处理#	
def preprocess(input_dir,input_file):
	pro_str=''
	temp_1line_file=input_file.split('.')[0]+'_1line.txt'
	infp=open(input_dir+'/'+input_file,'r')
	if not os.path.exists('../temp'):
		os.mkdir('../temp')
	tempfp=open('../temp/'+temp_1line_file,'w')
	for line in infp.readlines():
		#print str(len(line))+'\t'+line
		if len(line)>LEN_MIN:
			pro_str+=line
	pro_str=re.sub(r'[\n|\r]','',pro_str)
	tempfp.write(pro_str)
	infp.close()
	tempfp.close()
	print i
	return temp_1line_file	
	
fs=[]
for root,dirs,files in os.walk(input_dir):
	for fn in files:
		fs.append(os.path.join(root,fn))
		
for f in fs:
	input_file=f.split('\\')[-1]
	output_file=input_file.split('.')[0]+'_re.txt'
	temp_1line_file=preprocess(input_dir,input_file)
	cmd='python sbd.py -m model_nb ../temp/'+temp_1line_file+' -o '+output_dir+'/'+output_file
	os.system(cmd)
	i+=1
	
	
'''
使用本程序时，应先所有Input的文件至于input_dir的根目录下
且本程序仅在splitta文件目录下运行时有效
若运行出错，很可能是路径问题
'''
