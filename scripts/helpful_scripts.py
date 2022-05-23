from brownie import accounts, network, config
from eth_typing import HexStr
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(accounts[0].balance())
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


# initializer#box.store, 1,2,3,4,5,
def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([bronie.network.contractTx], optional):
        The inicializer function we want to call, Example: `box.store`.
        Defaults to None

        args (Any, optional):
        The arguments to pass to the initializer function

    Returns:
        [bytes]: Return the encoded bytes.

    """
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)

# From here we're going to start works with functions on BoxV2

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call =encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            trasaction = proxy_admin_contract.upgrade(proxy.address, new_implementation_address, {"from": account})
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy,upgradeToAndCall(new_implementation_address, encoded_function_call, {"from": account})
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from": account})
    return transaction