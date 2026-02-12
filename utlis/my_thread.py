import threading
import traceback

from tour.tour_line_fix import TourLineFixGenerator
from tour.tour_line_arount import TourLineArount
from tour.tour_line_follow import TourLineFollow
from tour.tour_line_follow_mode import TourLineFollowMode


class ThreadLine(threading.Thread):
    """线路生成线程"""
    
    def __init__(self, kmlname, tour_type, tour_time, length, distance, coords, is_mode=False):
        super().__init__()
        self.kmlname = kmlname
        self.is_mode = is_mode
        self.tour_type = tour_type
        self.tour_time = tour_time
        self.coords = coords
        self.length = length
        self.distance = distance
        self.on_complete = None  # 完成回调函数
        self._status = False
    
    def run(self):
        """线程执行方法"""
        try:
            self.download_tour_line()
            self._status = True
        except Exception as e:
            traceback.print_exc()
            self._status = False
        
        # 调用完成回调
        if self.on_complete:
            self.on_complete(self._status)
    
    def download_tour_line(self):
        """
        下载/生成线路 KML 文件
        """
        if self.tour_type == "生长路线-固定视角":
            TourLineFixGenerator(self.kmlname).tour_generator(self.kmlname, self.tour_time, self.coords)
        elif self.tour_type == "生长路线-环绕视角":
            TourLineArount(self.kmlname).tour_line_arount(
                self.kmlname, self.coords,
                length=self.length,
                distance=self.distance,
                tour_time=self.tour_time
            )
        elif self.tour_type == "生长路线-跟随视角" and self.is_mode is True:
            TourLineFollowMode(self.kmlname).tour_line_follow(
                self.kmlname,
                coords=self.coords,
                length=self.length * 1,
                distance=self.distance,
                tour_time=self.tour_time
            )
        elif self.tour_type == "生长路线-跟随视角":
            TourLineFollow(self.kmlname).tour_line_follow(
                self.kmlname, self.coords,
                length=self.length,
                distance=self.distance,
                tour_time=self.tour_time
            )
