#!/usr/bin/env python2
import sys
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

# main
def main(argv):
    import getopt			#getopt 模块，它的功能是 获取执行命令行时附带的参数，关于getopt模块详细可参照http://www.16kan.com/post/207647.html
    def usage(): 			#usage() 函数，用于在用户输入错误命令或者命令输入不规范时，输出py文件的使用范例。当参数不足或错误时，usage()被调用
        print ('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output] [-C] '
               '[-n] [-A] [-V] [-M char_margin] [-L line_margin] [-W word_margin] [-F boxes_flow] '
               '[-Y layout_mode] [-O output_dir] [-t text|html|xml|tag] [-c codec] [-s scale] file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:t:c:s:')
		'''
		getopt函数的格式是getopt.getopt ( [命令行参数列表], "短选项", [长选项列表] )
		短选项名后的冒号(:)表示该选项必须有附加的参数。p,m,P,o,M,L,W,F,Y,O,t,c,s均为必须参数
		长选项名后的等号(=)表示该选项必须有附加的参数。
		返回opts和args。
		'''
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    # debug option
    debug = 0
    # input option
    password = ''			#参数P
    pagenos = set()			#参数p
    maxpages = 0			#参数m
    # output option
    outfile = None			#参数o output
    outtype = None			#参数t out type
    outdir = None			#参数O output directory
    layoutmode = 'normal'	#参数Y
    codec = 'utf-8'			#参数c
    pageno = 1				
    scale = 1				#参数s,暂缺M,L,F,Y四个参数
    caching = True
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-C': caching = False
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-V': laparams.detect_vertical = True
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-F': laparams.boxes_flow = float(v)
        elif k == '-Y': layoutmode = v
        elif k == '-O': outdir = v
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:				#确认输出文件格式
        outtype = 'text'
        if outfile:			
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:					
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)  #TextConverter貌似不能指定outdir参数
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, outdir=outdir)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams, outdir=outdir)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return usage()
    for fname in args:
        fp = file(fname, 'rb')
        process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                    caching=caching, check_extractable=True)
        fp.close()
    device.close()
    outfp.close()
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
