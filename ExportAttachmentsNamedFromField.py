"""
ExportAttachmentsFilenameFromField.py
Exports Survey123 attachments, saving them with filenames defined by
an attribute value. Assumes attachments are jpg.
NW Oct 2019
"""

import arcpy
import pandas as pd
import os

# ArcGIS Script Tool parameters
fc_table = arcpy.GetParameterAsText(0) # Feature class to which attachments are
                                       # related
attach_table = arcpy.GetParameterAsText(1) # S123 attachment table. Should be
                                           # suffixed with _ATTACH
field_name = arcpy.GetParameterAsText(2) # field name to derive filenames from
output_folder = arcpy.GetParameterAsText(3) # where to save output files

attach_table_fields = ['REL_GLOBALID', 'ATTACHMENTID', 'DATA', 'ATT_NAME']
attach_table_df = pd.DataFrame()
att_name_list = []

# loop through attachment table and save all records to disk
arcpy.AddMessage('Exporting attachment data...')
with arcpy.da.SearchCursor(attach_table, attach_table_fields) as c:
    for row in c:
        attachment = row[2]
        filename = row[3]
        if os.path.isfile(output_folder + os.sep + filename):
            arcpy.AddMessage('Error: Cannot export: File {} already exists'.format(filename))
        else:
            try:
                open(output_folder + os.sep + filename, 'wb').write(attachment.tobytes())

                # Create pandas dataframe of tabular data
                attach_table_df = attach_table_df.append({'ID': row[0],
                                                          'ATT_NAME': row[3],
                                                          'ATTACHMENTID': row[1]},
                                                          ignore_index=True)
                att_name_list.append(row[3])

            except Exception as e:
                arcpy.AddMessage('Error:')
                arcpy.AddMessage(e)

fc_fields = ['GLOBALID', field_name]
fc_df = pd.DataFrame()

# loop through feature class attribute table and create pandas df of data
with arcpy.da.SearchCursor(fc_table, fc_fields) as fc_c:
    for row in fc_c:
        fc_df = fc_df.append({'ID': row[0], 'Name': row[1]}, ignore_index=True)

# table join
try:
    attach_table_df = attach_table_df.merge(fc_df)
except:
    arcpy.AddMessage('Data join failed.')

# rename the exported files to attribute values
arcpy.AddMessage('Naming...')
for r, d, f in os.walk(output_folder):
    for file in f:

        if file in att_name_list:

            k = attach_table_df.loc[attach_table_df['ATT_NAME'] == file]

            try:
                attach_id = (attach_table_df.loc[attach_table_df['ATT_NAME'] ==
                             file]['ATTACHMENTID'].values[0])
                attach_id = str(int(attach_id))
            except Exception as e:
                arcpy.AddMessage('Error: Could not match data:')
                arcpy.AddMessage(e)

            # output filename = field specified by user, plus attachment id to
            # ensure unique filename
            output_name = (attach_table_df.loc[attach_table_df['ATT_NAME'] ==
                           file]['Name'].values[0])
            output_name = output_name.replace(' ', '_')
            output_name = output_name.replace('(', '')
            output_name = output_name.replace(')', '')
            output_name = output_name.replace('.', '')
            output_name = output_name.replace(',', '')
            output_name = output_name + '_' + attach_id + '.jpg'


            if os.path.isfile(output_folder + os.sep + output_name):
                arcpy.AddMessage('Error: Cannot rename: File {} already exists'.
                                  format(output_name))
                pass
            else:
                try:
                    arcpy.AddMessage('Saving: {}'.format(output_name))
                    os.rename(output_folder + os.sep + file,
                              output_folder + os.sep + output_name)

                except Exception as e:
                    arcpy.AddMessage('Error:')
                    arcpy.AddMessage(e)

            del output_name
del att_name_list
del fc_df
del attach_table_df
arcpy.AddMessage('Script complete')
