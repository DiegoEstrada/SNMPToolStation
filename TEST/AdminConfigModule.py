import ConfigurationAdmin

def main():
    a = ConfigurationAdmin.ConfigurationAdmin("192.168.202.5/24",
                            "192.168.202.15",
                            {"192.168.202.0/24""ospf-R3.startup-config.txt"},
                            "tap0")
    print(a)
    #res = a.verifyConnection()

    #######Adding new rules to connect ########
    #a.addRule("192.168.232.4/30")
    #a.addRule("192.168.232.8/30")
    #res = a.verifyConnection("192.168.232.10")
    #a.downloadConfigFile()
    #a.uploadConfigFile("a.txt")
    #d = a.querySNMPInfo()
    #print(d)
    a.verifyLastVersion()
if __name__ == "__main__":
    main()