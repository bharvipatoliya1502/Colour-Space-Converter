-- Optional sample records for a fresh database.
INSERT INTO images(filename,uploaded_at,width,height,file_format)
VALUES('sample_demo.png','2026-01-01T10:00:00',2,2,'PNG');
INSERT INTO colour_spaces(image_id,source_space,target_space,matrix_name,created_at,matrix_values,determinant,matrix_rank)
VALUES(last_insert_rowid(),'RGB','YIQ','RGB_TO_YIQ_3x3','2026-01-01T10:00:01',
'[[0.299,0.587,0.114],[0.596,-0.274,-0.322],[0.211,-0.523,0.312]]',-0.253894,3);
INSERT INTO conversions(image_id,operation,mae,rmse,status,created_at)
VALUES(1,'RGB to YIQ to RGB',0.0,0.0,'success','2026-01-01T10:00:02');
