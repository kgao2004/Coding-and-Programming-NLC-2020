:: SQLite Backup Script (run in task scheduler daily)

:: This will create a timestamp like mm-dd-yyyy-hh-mm-ss
set PROJECTFOLDER=C:\Users\Karen Gao\OneDrive\PycharmProjects\community_service_program
set BACKUPFOLDER=%PROJECTFOLDER%\sqlite_backup_folder\%DATE:~4,2%-%DATE:~7,2%-%DATE:~10,4%-%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%

:: Create a new folder named with the timestamp
md "%BACKUPFOLDER%"

:: Copy database into backup folder
copy "%PROJECTFOLDER%\hours_tracker\db.sqlite3" "%BACKUPFOLDER%"

