import ConfigurationAdmin

def main():
    a = ConfigurationAdmin.ConfigurationAdmin("192.168.0.1/24",
                            "192.168.203.15",
                            {"192.168.0.0/24","ospf-R3.startup-config.txt"},
                            "tap0")
    print(a)

if __name__ == "__main__":
    main()