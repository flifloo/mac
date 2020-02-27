from pymysql import connect
from ipaddress import IPv4Network
from randmac import RandMac
from sys import stderr, argv
from subprocess import run, PIPE


DB_HOST = ""
DB_USER = ""
DB_PASS = ""
DB_NAME = ""

SSH_HOST = ""
SSH_PORT = ""
SSH_KEY = ""
SSH_USER = ""

DEFAULT_INTERFACE = ""

debug = False

if debug:
	print("DEBUG MOD ACTICATED !")

def main(args):
	"""
	args: list
		List of IP prefix

	This function get from DB and routeur IPs and MACs, create insertion list and sent it
	"""

	# DB connection
	try:
		print("Connect to DB...")
		db = connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
		cursor = db.cursor()
	except:
		print("Can't connect to DB !", file=stderr)
		exit(1)
	else:
		print("Connected to DB")

	# Get IPs from DB
	try:
		print("Get IPs...")
		cursor.execute("SELECT ip FROM mg_proxmox_addon_ip")
		ipRow = cursor.fetchall()
		ipRow = [i[0] for i in ipRow]
	except:
		print("Failt to get IPs !", file=stderr)
		exit(1)
	else:
		print("IPs get")

	# Get MACs from DB
	try:
		print("Get MACs...")
		cursor.execute("SELECT mac_address FROM mg_proxmox_addon_ip")
		macRow = cursor.fetchall()
		macRow = [i[0] for i in macRow]
	except:
		print("Fail to get MACs !", file=stderr)
		exit(1)
	else:
		print("MACs get")

	# Get IPs and MACs from routeur
	try:
		print("Get routeur IPs and MACs...")
		routeur = run(["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking no", f"{SSH_USER}@{SSH_HOST}", "-p", SSH_PORT, "/ip arp print"], stdout=PIPE).stdout.decode()
	except:
		print("Failt to get reouteur IPs and MACs !", file=stderr)
		exit(1)
	else:
		print("Routeur IPs and MACs get")

	cursor.close()

	# Get vlan give on the first arg
	vlan = args[0]
	if vlan != "null":
		try:
			vlan = int(vlan)
		except:
			print("Invalid vlan !", file=stderr)
			exit(1)
	del args[0]

	# Get list of ip, mac and subnet_mask to add
	out = []
	for arg in args:
		out+=addIPs(arg, ipRow, macRow)

	# Insert the list
	print(f"Start insert of {len(out)} IPs")
	insertIPs(out, vlan, db, routeur)


def addIPs(prefix: str, ipRow: [str], macRow: [str]) -> [(str, str, str, int)]:
	"""
	prefix: str
		The IPs prefix
	ipRow: list of str
		A list of IPs in the DB
	macRow: list of string
		A list of MACs in the DB
	return: List of tupple with IP, MAC, subnet_mask and cidr

	This function generate a lits of IPs and MACs to insert
	"""
	out = []

	# Check if prefix is valid
	try:
		print(f"Get IPs for {prefix}")
		ips = IPv4Network(prefix)
		subnet_mask = ips.netmask
		cidr = ips.prefixlen
	except:
		print("Invalid IP prefix !", file=stderr)
	else:
		# For all ip in prefix
		for ip in ips.hosts():
			# Check DB
			if str(ip) not in ipRow:
				# Random until not in DB
				mac = RandMac("00:00:00:00:00:00", True)
				while mac in macRow:
					mac = RandMac()
				# Append to shared list to avoid colisions
				ipRow.append(ip)
				macRow.append(mac)

				out.append((str(ip), str(mac), str(subnet_mask), int(cidr)))

			else:
				print(f"IP: {ip} already on DB !", file=stderr)
		print(f"Got {len(out)} IPs")	
	return out


def insertIPs(insert: [(str, str, str, int)], vlan, db, routeur):
	"""
	insert: List of tupple with IP, MAC and subnet_mask
		The list of IPs, MACs to insert
	db: MySQL DB object
		The DB to insert
	routeur: str
		A string content MACs and IPs content in routeur

	This function insert given IPs and MACs to SB and routeur (if necessary)
	"""
	cursor = db.cursor()

	# For every IP to insert
	gateway = insert[0][0]
	del insert[0]
	print(f"Use gateway: {gateway}")
	for i in insert:
		# Try insert into DB
		try:
			cmd = f"INSERT INTO mg_proxmox_addon_ip (ip, type, mac_address, subnet_mask, cidr, gateway, tag) VALUES ('{i[0]}', 'IPv4', {i[1]}, '{i[2]}', {i[3]}, '{gateway}', {vlan})"
			if debug:
				print(cmd)
			cursor.execute(cmd)
		except Exception as e:
			raise e
			print(f"Fail to insert values !\nIP: {i[0]}, Type: IPv4, MAC: {i[1]}, subnet_mask: {i[2]}", file=stderr)
		else:
			# Optional log
			#print(f"IP: {i[0]} of type IPv4 with MAC: {i[1]} on subnet_mask: {i[2]} add")

			# If IP and MAC ar not in the routeur, add them
			if ((i[0] not in routeur) or not (routeur[routeur.find(i[0]):5].replace(" ", ""))) and (i[1] not in routeur):
				if vlan != "null":
					interface = f"vlan{vlan}"
				else:
					interface = DEFAULT_INTERFACE

				cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking no", f"{SSH_USER}@{SSH_HOST}", "-p", SSH_PORT, f"/ip arp add address={i[0]} mac-address={i[1]} interface={interface}".replace("'", "")]
				if debug:
					print(cmd)
				else:
					run(cmd)
			elif debug:
				print(f"Already on the routeur !\nIP: {i[0]}, Type: IPv4, MAC: {i[1]}, subnet_mask: {i[2]}", file=stderr)

	cursor.close()

	# Commit to the DB
	if debug:
		print("Commit DB...")
	else:
		try:
			print("Commit to DB...")
			db.commit()
		except:
			print("Fail to commit !", file=stderr)
			exit(1)
		else:
			print("Commited to DB")



# Execution as a script handler
if __name__ == "__main__":
	# Avoid file name on args
	if argv[0] == __file__:
		del argv[0]

	# Start main function
	main(argv)
