#The purpose of this script is to fishnet a large DEM layer, run the contours tool on each fishnet, and then append them all together.
# It sounds simple, but required several nested for loops, lists, and time to get right.

import os
import sys
import string
import arcpy
from arcpy import env
from arcpy.sa import *
import arcpy.cartography as CA
import datetime
import collections
arcpy.env.overwriteOutput = True


class Contour_Processing:
	def __init__(self, DEM, mask1, mask2):
		self.DEM = DEM
		self.mask1 = mask1
		self.mask2 = mask2

	def Workspace_Iterator(self):

		gdb_list = os.listdir(r"C:\Users\ahimmelberger\Documents\Contours_Big1" )
		self.temp = r"C:\Users\ahimmelberger\Documents\Contours_Big1"  + "\\" + "Temp.gdb"
		for gdb in gdb_list:
			if gdb.endswith(".gdb"):
				if gdb.endswith("Temp.gdb"):
					pass
				else:	
					self.index_fc_start = r"C:\Users\ahimmelberger\Documents\Contours_Big1" + "\\" + gdb + "\\" + "Starting_Square"
					self.fishnet = r"C:\Users\ahimmelberger\Documents\Contours_Big1" + "\\" + gdb + "\\" + "Fishnet"
					print self.temp
					print "Working on gdb {0}...".format(gdb)
					print datetime.datetime.now()
					self.Fishnet_Setup()


	def Fishnet_Setup(self):
		# counting
		feats_list = []
		clip_list = []
		contour_list = []
		smooth_list = []
		eight_list = []
		dissolve_list = []
		contour_list_cleaned = []
		PRE_FINAL_list = []
		FINAL_list = []
		FINAL_FINAL_list = []
		new_smooth_list = []
		fish_list = []
		count = 0
		feature_count = len(list(i for i in arcpy.da.SearchCursor(self.fishnet, ["ORIG_FID"])))
		print "Total feature_count is {0}".format(str(feature_count))
		for x in xrange(1000):
			if x == 0:
				# build the temp vars
				clip_path = os.path.dirname(self.fishnet) + "\\" + "ContourClip_test_" + str(x)
				main_contour = os.path.dirname(self.fishnet) + "\\" + "MainContour"
				main_fish = os.path.dirname(self.fishnet) + "\\" + "MainFish"
				arcpy.Copy_management(self.index_fc_start, main_fish)
				# Extract by mask and contour
				arcpy.CheckOutExtension("Spatial")
				outExtractByMask = ExtractByMask(self.DEM, self.index_fc_start)   
				outExtractByMask.save(clip_path)
				Contour(clip_path, main_contour, 20, "", "")
				#Clean inital contours layer from values exactly equal to round numbers. These are errors.
				contour_fields1 = ['Shape_Length']
				main_contour_cleaned = os.path.dirname(self.fishnet) + "\\" + "MainContour_Cleaned"
				contour_lyr1 = str("MainContour")
				arcpy.MakeFeatureLayer_management(main_contour, contour_lyr1)
				arcpy.SelectLayerByAttribute_management(contour_lyr1, "NEW_SELECTION", "(Shape_Length >5.001) AND (Shape_Length < 9.999 OR Shape_Length >10.001) AND (Shape_Length < 14.9 OR Shape_Length >15.001) AND (Shape_Length < 19.999 OR Shape_Length >20.001) AND (Shape_Length < 24.999 OR Shape_Length >25.001) AND (Shape_Length < 29.999 OR Shape_Length >30.001) AND (Shape_Length < 30.999 OR Shape_Length >35.001) AND (Shape_Length < 39.999 OR Shape_Length >40.001) AND (Shape_Length < 44.999 OR Shape_Length >45.001) AND (Shape_Length < 49.999 OR Shape_Length >50.001)  ")
				arcpy.CopyFeatures_management(contour_lyr1, main_contour_cleaned)
				#Smooth the main contour
				main_smooth = os.path.dirname(self.fishnet) + "\\" + "MainSmoothedContour"
				dissolve_list.append(main_smooth)
				CA.SmoothLine(main_contour_cleaned, main_smooth, "PAEK", 50, "", "FLAG_ERRORS")   
				# Note taking
				clip_list.append(clip_path)
				contour_list.append(main_contour_cleaned)
				with arcpy.da.SearchCursor(self.index_fc_start, "ORIG_FID") as sCursor:
					for sir in sCursor:
						feats_list.append(sir)
			elif len(feats_list) >= feature_count:
				arcpy.CheckInExtension("Spatial")
				for clip in clip_list:
					arcpy.Delete_management(clip)
				for contour in contour_list:
					arcpy.Delete_management(contour)
				for smooth in smooth_list:
					arcpy.Delete_management(smooth)
				for contour2 in contour_list_cleaned:
					arcpy.Delete_management(contour2)
				for contour in new_smooth_list:
					arcpy.Delete_management(contour2)
				for dissolved in dissolve_list:
					arcpy.Delete_management(dissolved)	
				for contour in PRE_FINAL_list:
					arcpy.Delete_management(contour)
				for contour in FINAL_list:
					arcpy.Delete_management(contour)
				del FINAL_FINAL_list[-1]	
				for contour in FINAL_FINAL_list:
					arcpy.Delete_management(contour)
				arcpy.Delete_management(first_fish)
				for fish in fish_list:
					arcpy.Delete_management(fish)
				break
			else:
				# Select and build the fc
				fish_lyr = arcpy.MakeFeatureLayer_management(self.fishnet, 'fishy_lyr')
				fish_sel = arcpy.SelectLayerByLocation_management(fish_lyr, "CROSSED_BY_THE_OUTLINE_OF", main_fish, "", "NEW_SELECTION")
				fish_fc = r"Fish_" + str(x)
				fish_fc_full = self.temp + "\\" + fish_fc
				first_fish = self.temp + "\\" + "Fish_1"
				fish_list.append(fish_fc_full)
				if os.path.exists(fish_fc_full) is True:
					arcpy.Delete_management(fish_fc_full)
				if os.path.exists(first_fish) is True:
					arcpy.Delete_management(first_fish)
				if os.path.exists(fish_fc) is True:
				 	arcpy.Delete_management(fish_fc)
				arcpy.FeatureClassToFeatureClass_conversion(fish_sel, self.temp, fish_fc)
				# Update the selection
				with arcpy.da.UpdateCursor(fish_fc_full, "ORIG_FID") as cursor:
					for row in cursor:
						if row[0] in feats_list:
							cursor.deleteRow()
						else:
							feats_list.append(row[0])
				#Another update cursour
				fishnet_fields = ['ORIG_FID','SHAPE@','Shape_Length']
				with arcpy.da.SearchCursor(fish_fc_full, fishnet_fields) as cursor2:
					for polygon in cursor2:
						# Clip and contour
						clip_path = self.temp + "\\" + "ContourClip_" + str(count)
						outExtractByMask = ExtractByMask(self.DEM, polygon[1])   
						outExtractByMask.save(clip_path)
						contour_path = os.path.dirname(self.fishnet) + "\\" + "ContourReal_" + str(count)
						Contour(clip_path, contour_path, 20, "", "")
						#Copy lines more than 20 meters
						arcpy.env.workspace = os.path.dirname(self.fishnet)
						arcpy.env.mask = self.mask2
						#Cleaninng the contours
						contour_fields2 = ['Shape_Length']
						contour_path_cleaned = os.path.dirname(self.fishnet) + "\\" + "Contour_Cleaned_" + str(count)
						contour_lyr = str("Contour_Cleaned_" + str(count))
						arcpy.MakeFeatureLayer_management(contour_path, contour_lyr)
						arcpy.SelectLayerByAttribute_management(contour_lyr, "NEW_SELECTION", "(Shape_Length >5.001) AND (Shape_Length < 9.999 OR Shape_Length >10.001) AND (Shape_Length < 14.9 OR Shape_Length >15.001) AND (Shape_Length < 19.999 OR Shape_Length >20.001) AND (Shape_Length < 24.999 OR Shape_Length >25.001) AND (Shape_Length < 29.999 OR Shape_Length >30.001) AND (Shape_Length < 30.999 OR Shape_Length >35.001) AND (Shape_Length < 39.999 OR Shape_Length >40.001) AND (Shape_Length < 44.999 OR Shape_Length >45.001) AND (Shape_Length < 49.999 OR Shape_Length >50.001) AND (Shape_Length < 54.999 OR Shape_Length >55.001) AND (Shape_Length < 59.999 OR Shape_Length >60.001) AND (Shape_Length < 64.999 OR Shape_Length >65.001) AND (Shape_Length < 69.999 OR Shape_Length >70.001) AND (Shape_Length < 74.999 OR Shape_Length >75.001)AND (Shape_Length < 79.999 OR Shape_Length >80.001) AND (Shape_Length < 84.999 OR Shape_Length >85.001) AND (Shape_Length < 89.999 OR Shape_Length >90.001) AND (Shape_Length < 94.999 OR Shape_Length >95.001) AND (Shape_Length < 99.999 OR Shape_Length >100.001) AND (Shape_Length < 104.999 OR Shape_Length >105.001) AND (Shape_Length < 109.999 OR Shape_Length >110.001) AND (Shape_Length < 114.999 OR Shape_Length > 115.001) AND (Shape_Length < 119.999 OR Shape_Length >120.001) AND (Shape_Length < 124.999 OR Shape_Length >125.001) AND (Shape_Length < 129.999 OR Shape_Length >130.001) AND (Shape_Length < 134.999 OR Shape_Length >135.001) AND (Shape_Length < 139.999 OR Shape_Length >140.001) AND (Shape_Length < 144.999 OR Shape_Length >145.001) AND (Shape_Length < 149.999 OR Shape_Length >150.001)")
						arcpy.CopyFeatures_management(contour_lyr, contour_path_cleaned)
						arcpy.env.workspace = os.path.dirname(self.fishnet)
						arcpy.env.mask = ""
						#Counting contours
						count_lyr = str("Contour_count_" + str(count))
						arcpy.MakeFeatureLayer_management(contour_path_cleaned, count_lyr)
						result = arcpy.GetCount_management(count_lyr)
						count2 = int(result.getOutput(0))
						#smooth Lines
						if count2 != 0:
							smooth_path = os.path.dirname(self.fishnet) + "\\" + "SmoothedContour_" + str(count)
							CA.SmoothLine(contour_path_cleaned, smooth_path, "PAEK", 50, "", "FLAG_ERRORS")
							# Snap and append
							used_smooth = dissolve_list[-1:]
							new_smooth = os.path.dirname(self.fishnet) + "\\" + "Dissolved_FINAL_OUTPUT" + str(count)
							dissolve_list.append(new_smooth)
							arcpy.env.workspace = os.path.dirname(self.fishnet)
							arcpy.env.mask = self.mask1
							arcpy.Snap_edit(smooth_path, [[used_smooth[0], "END","10 Meters"]])
							arcpy.Append_management(smooth_path, used_smooth[0], "NO_TEST")
							arcpy.Append_management(polygon[1], main_fish, "NO_TEST")
							dissolve_fields = ["Contour"]
							arcpy.env.mask = ""
							arcpy.Dissolve_management(used_smooth[0], new_smooth, dissolve_fields, multi_part="SINGLE_PART")
							#Clean_up
							contour_fields3 = ['Shape_Length']
							PRE_FINAL_contours = os.path.dirname(self.fishnet) + "\\" + "PRE_FINAL_CONTOUR" + str(count)
							arcpy.env.workspace = os.path.dirname(self.fishnet)
							arcpy.env.mask = self.mask2
							contour_lyr3 = str("PRE_FINAL_CONTOUR" + str(count))
							arcpy.MakeFeatureLayer_management(new_smooth, contour_lyr3)
							arcpy.SelectLayerByAttribute_management(contour_lyr3, "NEW_SELECTION", "(Shape_Length >5.001) AND (Shape_Length < 9.999 OR Shape_Length >10.001) AND (Shape_Length < 14.9 OR Shape_Length >15.001) AND (Shape_Length < 19.999 OR Shape_Length >20.001) AND (Shape_Length < 24.999 OR Shape_Length >25.001) AND (Shape_Length < 29.999 OR Shape_Length >30.001) AND (Shape_Length < 30.999 OR Shape_Length >35.001) AND (Shape_Length < 39.999 OR Shape_Length >40.001) AND (Shape_Length < 44.999 OR Shape_Length >45.001) AND (Shape_Length < 49.999 OR Shape_Length >50.001) AND (Shape_Length < 54.999 OR Shape_Length >55.001) AND (Shape_Length < 59.999 OR Shape_Length >60.001) AND (Shape_Length < 64.999 OR Shape_Length >65.001) AND (Shape_Length < 69.999 OR Shape_Length >70.001) AND (Shape_Length < 74.999 OR Shape_Length >75.001)AND (Shape_Length < 79.999 OR Shape_Length >80.001) AND (Shape_Length < 84.999 OR Shape_Length >85.001) AND (Shape_Length < 89.999 OR Shape_Length >90.001) AND (Shape_Length < 94.999 OR Shape_Length >95.001) AND (Shape_Length < 99.999 OR Shape_Length >100.001) AND (Shape_Length < 104.999 OR Shape_Length >105.001) AND (Shape_Length < 109.999 OR Shape_Length >110.001) AND (Shape_Length < 114.999 OR Shape_Length > 115.001) AND (Shape_Length < 119.999 OR Shape_Length >120.001) AND (Shape_Length < 124.999 OR Shape_Length >125.001) AND (Shape_Length < 129.999 OR Shape_Length >130.001) AND (Shape_Length < 134.999 OR Shape_Length >135.001) AND (Shape_Length < 139.999 OR Shape_Length >140.001) AND (Shape_Length < 144.999 OR Shape_Length >145.001) AND (Shape_Length < 149.999 OR Shape_Length >150.001)")
							arcpy.CopyFeatures_management(contour_lyr3, PRE_FINAL_contours)
							arcpy.env.mask = ""
							#Dissolve 1st time
							FINAL_contours = os.path.dirname(self.fishnet) + "\\" + "FINAL_CONTOUR" + str(count)
							arcpy.Dissolve_management(PRE_FINAL_contours, FINAL_contours, dissolve_fields, multi_part="SINGLE_PART")
							#Clean up one last time
							arcpy.env.workspace = os.path.dirname(self.fishnet)
							arcpy.env.mask = self.mask2
							FINAL_FINAL_contours = os.path.dirname(self.fishnet) + "\\" + "FINAL_FINAL_CONTOUR" + str(count)
							contour_lyr4 = str("FINAL_FINAL_CONTOUR" + str(count))
							arcpy.MakeFeatureLayer_management(FINAL_contours, contour_lyr4)
							arcpy.SelectLayerByAttribute_management(contour_lyr4, "NEW_SELECTION", "(Shape_Length >5.6) AND (Shape_Length < 9.5 OR Shape_Length >10.5) AND (Shape_Length < 14.5 OR Shape_Length >15.5) AND (Shape_Length < 19.5 OR Shape_Length >20.5) AND (Shape_Length < 24.5 OR Shape_Length >25.5) AND (Shape_Length < 29.5 OR Shape_Length >30.5) AND (Shape_Length < 30.5 OR Shape_Length >35.5) AND (Shape_Length < 39.5 OR Shape_Length >40.5) AND (Shape_Length < 44.5 OR Shape_Length >45.5) AND (Shape_Length < 49.5 OR Shape_Length >50.5) AND (Shape_Length < 54.5 OR Shape_Length >55.5) AND (Shape_Length < 59.5 OR Shape_Length >60.5) AND (Shape_Length < 64.5 OR Shape_Length >65.5) AND (Shape_Length < 69.5 OR Shape_Length >70.5) AND (Shape_Length < 74.5 OR Shape_Length >75.5) AND (Shape_Length < 79.5 OR Shape_Length >80.5) AND (Shape_Length < 84.5 OR Shape_Length >85.5) AND (Shape_Length < 89.5 OR Shape_Length >90.5) AND (Shape_Length < 94.5 OR Shape_Length >95.5) AND (Shape_Length < 99.5 OR Shape_Length >100.5) AND (Shape_Length < 104.5 OR Shape_Length >105.5) AND (Shape_Length < 109.5 OR Shape_Length >110.5)  AND (Shape_Length < 110.5 OR Shape_Length >115.5)  AND (Shape_Length < 119.5 OR Shape_Length >120.5) AND (Shape_Length < 124.5 OR Shape_Length >125.5) AND (Shape_Length < 129.5 OR Shape_Length >130.5) AND (Shape_Length < 134.5 OR Shape_Length >135.5) AND (Shape_Length < 139.5 OR Shape_Length >140.5) AND (Shape_Length < 144.5 OR Shape_Length >145.5) AND (Shape_Length < 149.5 OR Shape_Length >150.5)")
							arcpy.CopyFeatures_management(contour_lyr4, FINAL_FINAL_contours)
							arcpy.env.mask = ""

							#Dissolve into final layer
							arcpy.Dissolve_management(FINAL_contours, FINAL_FINAL_contours, dissolve_fields, multi_part="SINGLE_PART")

						# Note taking
							clip_list.append(clip_path)
							contour_list.append(contour_path)
							smooth_list.append(smooth_path)
							contour_list_cleaned.append(contour_path_cleaned)
							new_smooth_list.append(new_smooth)
							PRE_FINAL_list.append(PRE_FINAL_contours)
							FINAL_list.append(FINAL_contours)
							FINAL_FINAL_list.append(FINAL_FINAL_contours)
							count += 1		
						

if __name__ == "__main__":
	DEM = r"F:\Anthony\Projects\Contours\nor_hls_5m"
	mask1 = r"C:\Users\ahimmelberger\Documents\Contours\FINAL_CONTOURS_RUN.gdb\Snapping_Mask"
	mask2 = r"C:\Users\ahimmelberger\Documents\Contours\FINAL_CONTOURS_RUN.gdb\Cleaning_Mask"
	# index fc is any single polygon in the fishnet that lies near the center of the grid
	create_contours = Contour_Processing(DEM, mask1, mask2)
	create_contours.Workspace_Iterator()
