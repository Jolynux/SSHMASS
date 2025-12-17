import functions as fc


############### Vars ###############

df_excel = fc.extract_excel_data()
username = str(input("Username : "))
password = str(getpass.getpass(prompt="Password : ", stream=None))


############### Menu ###############

print("""
1 - Execute command on hosts
2 - Launch a script
3 - Send file or directory
* - Quit
""")

choice = input("Choice N° ").strip()

match choice:
    case "1":
        action = "command"
        command = input("▶️ Command to execute : ")

    case "2":
        action = "script"
        script_path = input("📜 Local script path : ")

    case "3":
        action = "upload"
        local_path = input("📂 Local file path : ")
        remote_path = input("📂 Remote destination path : ")

    case _:
        print("🏁 Exiting SSHMASS")
        exit(0)


############### Main ###############

df_excel["Output"] = ""
df_excel["Status"] = ""

for index, row in df_excel.iterrows():
    print(f"🔄 Connecting to {row["Host"]}")

    try:
        output = fc.ssh_action(
            host=row["Host"],
            username=username,
            password=password,
            action=action,
            command=command if action == "command" else None,
            script_path=script_path if action == "script" else None,
            local_path=local_path if action == "upload" else None,
            remote_path=remote_path if action == "upload" else None
        )

        df_excel.at[index, "Output"] = output
        df_excel.at[index, "Status"] = "🟢 SUCCESS"
        print(f"🟢 Success on {row["Host"]}")

    except Exception as e:
        df_excel.at[index, "Output"] = str(e)
        df_excel.at[index, "Status"] = "🔴 ERROR"
        print(f"🔴 Error on {row["Host"]}: {e}")
