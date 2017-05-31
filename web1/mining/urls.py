# coding: utf-8
from views import *

url_handlers = [
    (r"^/$", Defect_Mining_Binarys_Page_Handler),
    # 二进制文件上传
    (r"/mining/binary_upload", Defect_Mining_Binary_Upload_Handler),
    # 二进制文件开始
    (r"/mining/binary_start", Defect_Mining_Binary_Start_Handler),
    # 二进制文件删除
    (r"/mining/binary_delete", Defect_Mining_Binary_Delete_Handler),

    # 二进制文件列表
    (r"/mining/binarys_data", Defect_Mining_Binarys_Data_Handler),
    (r"/mining/binarys", Defect_Mining_Binarys_Page_Handler),

    # 日志文件输出
    (r"/mining/logs_data", Defect_Mining_Logs_Data_Handler),
    (r"/mining/logs", Defect_Mining_Logs_Page_Handler),

    # 崩溃文件内容
    (r"/mining/crash_file", Defect_Mining_Crash_File_Handler),
]