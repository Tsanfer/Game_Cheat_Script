#! python3
# coding=utf-8
__name__ = "Plants vs. Zombies.air"
__title__ = "植物大战僵尸自动化脚本"
__author__ = "Tsanfer"
__desc__ = """
植物大战僵尸辅助通关脚本
配合 Cheat Engine 使用
"""

from xml.etree.ElementPath import ops
from airtest.core.api import *
from airtest.core.settings import Settings as ST  # 导入 Settings 设置
from airtest.aircv import *  # crop_image()方法在airtest.aircv中，需要引入


class default_back:
    """默认全局属性设置
    Attributes:
        find_timeout: Settings.FIND_TIMEOUT 默认值
        find_timeout_tmp: Settings.FIND_TIMEOUT_TMP 默认值
        snapshot_quality: Settings.SNAPSHOT_QUALITY 默认值
    """

    def __init__(self):
        """备份全局属性默认值，并打印"""
        self.find_timeout = ST.FIND_TIMEOUT
        self.find_timeout_tmp = ST.FIND_TIMEOUT_TMP
        self.snapshot_quality = ST.SNAPSHOT_QUALITY

        print("默认 ST.FIND_TIMEOUT = {}".format(self.find_timeout))
        print("默认 ST.FIND_TIMEOUT_TMP = {}".format(self.find_timeout_tmp))
        print("默认 ST.SNAPSHOT_QUALITY = {}".format(self.snapshot_quality))

    def __del__(self):
        """解构函数"""
        class_name = self.__class__.__name__
        print(class_name, "销毁", end="")

    def reset(self):
        """恢复默认函数值"""
        ST.FIND_TIMEOUT = self.find_timeout
        ST.FIND_TIMEOUT_TMP = self.find_timeout_tmp
        ST.SNAPSHOT_QUALITY = self.snapshot_quality


def image_match_in(image, origin_x=0, origin_y=0, x_length=800, y_length=600):
    """区域图片识别

    Args:
        image (Template): 图片
        origin_x (int, optional): 原点 x 坐标. Defaults to 0.
        origin_y (int, optional): 原点 y 坐标. Defaults to 0.
        x_length (int, optional): 窗口 x 长度. Defaults to 800.
        y_length (int, optional): 窗口 y 长度. Defaults to 600.

    Returns:
        list: 目标图像坐标
    """
    screen = dev.snapshot()  # 全窗口截图
    local_screen = aircv.crop_image(
        screen, (origin_x, origin_y, origin_x+x_length, origin_y+y_length))  # 裁剪局部图片
    # try_log_screen(local_screen)  # 保存局部截图到log文件夹中
    image_name = image.filename  # 获取图片文件名
    pos = Template(image_name).match_in(local_screen)  # 在局部截图里面，查找指定的图片对象
    pos = list(pos)  # 将元组转换为可编辑的列表
    pos[0] += origin_x  # x 坐标加上原点偏移
    pos[1] += origin_y  # y 坐标加上原点偏移
    return pos


def image_notfound():
    log("图片未找到")

# def custom_resize_method(w, h, sch_resolution, src_resolution):
#     return int(w), int(h)
# # 替换默认的RESIZE_METHOD
# ST.RESIZE_METHOD = custom_resize_method


def main():
    # 运行时只能有一个屏幕
    # 连接方式一
    auto_setup(__file__, devices=[
        "Windows:///?title_re=^Plants vs. Zombies$"])  # 正则表达式匹配连接窗口
    # 连接方式二
    # connect_device("Windows:///?title_re=Plants.*") # 运行时只能有一个屏幕

    global dev
    dev = device()
    dev.focus_rect = [0, 33, 0, 0]  # [左边框宽度，上边框宽度，右边框宽度，下边框宽度]
    print("窗口分辨率：", dev.get_current_resolution())
    print("窗口位置：", dev.get_pos())

    global default_val
    default_val = default_back()

    ST.FIND_TIMEOUT = ST.FIND_TIMEOUT_TMP  # 设置查询的超时时长
    # ST.SNAPSHOT_QUALITY = 70 # 设置脚本截图质量

    try:
        pos = image_match_in(Template(
            r"welcome_back.png", record_pos=(-0.289, -0.282), resolution=(800, 600)), 80, 60, 300, 150)
        touch(pos)
    #     touch(Template(r"home_option.png", record_pos=(0.329, 0.254), resolution=(731, 635)))
    #     pos = wait(Template(r"home_ok.png", record_pos=(-0.003, 0.219), resolution=(800, 600)), intervalfunc=image_notfound)
    #     touch(pos)
    #     touch(Template(r"home_option.png", record_pos=(0.329, 0.254), resolution=(731, 635)))
    #     keyevent("{ESC}")
    except AssertionError:
        log("当前位置不是主页")
    except Exception as e:
        log(e, snapshot=True)
    finally:
        log("End", snapshot=True)


# if __name__ == '__main__':
main()

