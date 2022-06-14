import json
from time import sleep

from hdwallet import HDWallet
from hdwallet.symbols import BTC
from btc_com import explorer as btc_explorer

# Update this to the path and filename of your text file containing private keys
TEXT_KEYFILE_PATH = "my_potential_btc_keys.txt"


def btc_address_from_private_key(my_secret, secret_type='WIF'):
    assert secret_type in ['WIF', 'classic', 'extended', 'mnemonic', 'mini']
    hdwallet = HDWallet(symbol=BTC)
    match secret_type:
        case 'WIF':
            hdwallet.from_wif(wif=my_secret)
        case 'classic':
            hdwallet.from_private_key(private_key=my_secret)
        case 'mnemonic':
            raise "Mnemonic secrets not implemented"
        case 'mini':
            raise "Mini private key not implemented"
        case 'extended':
            hdwallet.from_xprivate_key(xprivate_key=my_secret)
        case _:
            raise "I don't know how to handle this type."

    # Uncomment to print all Bitcoin HDWallet info
    # print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))

    return hdwallet.p2pkh_address()


def blockchain_com_url(btc_address):
    return 'https://www.blockchain.com/btc/address/' + btc_address


def btc_explorer_url(btc_address):
    return 'https://explorer.btc.com/btc/address/' + btc_address


def btc_explorer_api_url(btc_address):
    return 'https://chain.api.btc.com/v3/address/' + btc_address


def fetch_balance_for_btc_address(btc_address):
    # Get BTC balance from web API. This is rate limited
    address_info = btc_explorer.get_address(btc_address)
    sleep(10)  # To play nice with the API Rate limit
    return address_info.balance, address_info.tx_count


if __name__ == '__main__':

    try:
        # Assuming we have a plain text file with a potential key on each line.
        # Keys look like:
        # 6cd78b0d69eab1a47bfa53a52b9d8c4331e858b5d7a599270a95d9735fdb0b94
        fp = open(TEXT_KEYFILE_PATH)
        line = fp.readline()
        line_number = 1

        while line:
            my_secret = line.strip()
            # print("Secret {}: {}".format(line_number, my_secret))

            address = btc_address_from_private_key(my_secret, secret_type='classic')
            balance, tx_count = fetch_balance_for_btc_address(address)
            print(f"secret: {my_secret} address: {address} tx_count: {tx_count} balance: {balance}")

            line = fp.readline()
            line_number += 1

    finally:
        fp.close()


