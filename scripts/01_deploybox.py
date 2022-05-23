from base64 import encode
from scripts.helpful_scripts import get_account, encode_function_data, upgrade 
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2


# From Here we've manage to set up our proxy to be able to access our "2' contract BoxV2"
def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from":account}, publish_source = True)
    print(box.retrieve())

# Bellow here we're setting up a "proxy-admin" it is optional but is recommended to use one 
    proxy_admin = ProxyAdmin.deploy({"from":account}, publish_source = True)

    #initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer_function, {"from":account, "gas_limit": 1000000}, publish_source = True)
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2!") 
    proxy_box = Contract.from_abi("Boi", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

# From here we're going to start to access to functions on BoxV2
    box_v2 = BoxV2.deploy({"from": account}, publish_source = True)
    #Now to able to call our upgrade function we'll need to set first in helpful_scripts first
    upgrade_transaction = upgrade (account,proxy, box_v2.address, proxy_admin_contract=proxy_admin)
    #upgrade_transaction.wait(1)
    print("Proxy has been updated!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from":account})
    print(proxy_box.retrieve())
