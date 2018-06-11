from mig.io import ERDAShare, IDMCShare


def share_links_example():

    # Sharelinks lib Tutorial

    # ERDA Sharelink example
    print("ERDA")
    # Open connection to a sharelink
    erda_share = ERDAShare('SHARELINKID')
    # List files/dirs in share
    print(erda_share.list())

    with erda_share.open('tmp', 'w') as tmp:
        tmp.write("sdfsfsf")

    # Get a _io.SFTPFileHandle object with automatic close
    with erda_share.open('tmp', 'r') as tmp:
        print(tmp.read())

    # Get a default _io.SFTPFileHandle object with manual lifetime
    file = erda_share.open('tmp', 'r')
    print(file.read())
    file.close()

    # remove file
    erda_share.remove('tmp')

    print("\n")

    # IDMC Sharelink example
    print("IDMC")
    # Open connection to a sharelink
    idmc_share = IDMCShare('SHARELINKID')
    # List files/dirs in share
    print(idmc_share.list())

    # write binary string
    with idmc_share.open('b_tmp', 'wb') as b_tmp:
        b_tmp.write(b'sadasdasd')

    # Get a _io.SFTPFileHandle object with automatic close
    with idmc_share.open('b_tmp', 'rb') as tmp:
        print(tmp.read())

    # Get a default _io.TextIOWrapper object with manual lifetime
    file = idmc_share.open('b_tmp', 'rb')
    print(file.read())
    file.close()

    # remove file
    idmc_share.remove('b_tmp')


if __name__ == "__main__":
    share_links_example()
