import sys
import cv
import cv2
import numpy as npy

if __name__ == '__main__':
	vidFile = cv.CaptureFromFile('video.avi')

	nFrames = int (cv.GetCaptureProperty(vidFile,cv.CV_CAP_PROP_FRAME_COUNT))
	fps = cv.GetCaptureProperty(vidFile,cv.CV_CAP_PROP_FPS)
	waitPerFrameInMillisec = int(1/fps * 1000/1)
	width = int(cv.GetCaptureProperty(vidFile,cv.CV_CAP_PROP_FRAME_WIDTH))
	height = int(cv.GetCaptureProperty(vidFile,cv.CV_CAP_PROP_FRAME_HEIGHT))

	print 'Num. Frames = ',nFrames
	print 'Frame Rate = ',fps,	'frames per sec'

	camera_matrix = cv.CreateMat(3,3,cv.CV_32FC1)
	cv.SetReal2D(camera_matrix,0,0,469.96)
	cv.SetReal2D(camera_matrix,0,1,0.0)
	cv.SetReal2D(camera_matrix,0,2,640)
	cv.SetReal2D(camera_matrix,1,0,0.0)
	cv.SetReal2D(camera_matrix,1,1,467.68)
	cv.SetReal2D(camera_matrix,1,2,360)
	cv.SetReal2D(camera_matrix,2,0,0.0)
	cv.SetReal2D(camera_matrix,2,1,0.0)
	cv.SetReal2D(camera_matrix,2,2,1.0)

	dist_coeffs = cv.CreateMat(1,5,cv.CV_32FC1)
	cv.SetReal2D(camera_matrix,0,1,-0.018957)
	cv.SetReal2D(camera_matrix,0,1,0.037319)
	cv.SetReal2D(camera_matrix,0,1,0.0)
	cv.SetReal2D(camera_matrix,0,1,0.0)
	cv.SetReal2D(camera_matrix,0,1,0.00337)

	writer = cv.CreateVideoWriter(
			 filename = "output.avi"
			 fourcc =- 1
			 fps = fps
			 frame_size = (width,height)
			 is_color = 1
			 )

	map1 = cv.CreateImage((width,height),cv.IPL_DEPTH_32F,1)
	map2 = cv.CreateImage((width,height),cv.IPL_DEPTH_32F,1)
	cv.ImitUndistorMap(camera_matrix,dist_coeffs,map1,map2)

	for f in xrange(nFrames):
		frameImg = cv.QueryFrame(vidFile)
		if frameImg is None:
			print "Frame Nr", f, "fehlerhaft. Abbruch"
			break
		undistimage= cv.CloneImage(frameImg)
		cv.Remap(frameImg,undistimage,map1,map2)

		cv.ShowImage("Video",undistimatge)
		cv.WriteFrame(writer,undistimage)
		cv.WaitKey(waitPerFrameInMillisec)

		prozent = f*100/nFrames
		print prozent, "%"

		k= cv.WaitKey(1)
		if k % 0x100 == 27:
			break
		cv.DestroyWindow("Video")
		del writer

		


	
	