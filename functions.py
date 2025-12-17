import paramiko, os, pandas


def extract_excel_data():
    dfs = []

    for excel_file in os.listdir("./dir_input_excel"):
        if excel_file.endswith(".xlsx"):
            path = os.path.join("./dir_input_excel", excel_file)
            print(f"📂 Loading {excel_file}")
            dfs.append(pandas.read_excel(path))
        else:
            print(f"⚠️ Skipping non-xlsx file: {excel_file}")

    if not dfs:
        print("🔴 No .xlsx files found")
        sys.exit(1)

    return pandas.concat(dfs, ignore_index=True)

def ssh_action(host, username, password, action, command=None, script_path=None, local_path=None, remote_path=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, timeout=10)

    output = ""

    match action:
        case "command":
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode() + stderr.read().decode()

        case "script":
            script_name = os.path.basename(script_path)
            sftp = client.open_sftp()
            sftp.put(script_path, f"/tmp/{script_name}")
            sftp.chmod(f"/tmp/{script_name}", 0o755)
            sftp.close()

            stdin, stdout, stderr = client.exec_command(f"/tmp/{script_name}")
            output = stdout.read().decode() + stderr.read().decode()

        case "upload":
            sftp = client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            output = "File uploaded successfully"

        case _:
            raise ValueError("Unknown action")

    client.close()
    return output
