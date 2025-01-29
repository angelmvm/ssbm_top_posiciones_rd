import sys
sys.path.append("/home/user/scripts/modules")

from my_modules import General

log_path = "/home/user/scripts/melee_tournaments/logs/dr_tournaments*.log"

# Delete rd_tournament logs
General.delete_logs(log_path, 10)