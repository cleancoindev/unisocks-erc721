from test.constants import (
    DECIMALS,
    ERC165_INTERFACE_ID,
    ERC721_INTERFACE_ID,
)

def test_init(w3, SOCKS, UNISOCKS):
    a0, a1 = w3.eth.accounts[:2]
    assert UNISOCKS.name() == 'Digital Unisocks Edition 0'
    assert UNISOCKS.symbol() == 'S0CKS'
    assert UNISOCKS.totalSupply() == 0
    assert UNISOCKS.minter() == a0
    assert UNISOCKS.balanceOf(a1) == 0
    assert UNISOCKS.supportsInterface(ERC165_INTERFACE_ID) == True
    assert UNISOCKS.supportsInterface(ERC721_INTERFACE_ID) == True
    assert UNISOCKS.socks() == SOCKS.address

def test_transfer(w3, SOCKS, UNISOCKS, assert_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    assert_fail(lambda: UNISOCKS.mint(a1, transact={}))
    assert SOCKS.burn(2*DECIMALS, transact={})
    UNISOCKS.mint(a1, transact={})
    assert UNISOCKS.totalSupply() == 1
    UNISOCKS.mint(a2, transact={})
    assert UNISOCKS.totalSupply() == 2
    assert UNISOCKS.balanceOf(a1) == 1
    assert UNISOCKS.balanceOf(a2) == 1
    assert UNISOCKS.ownerOf(0) == a1
    assert UNISOCKS.ownerOf(1) == a2
    assert UNISOCKS.tokenOfOwnerByIndex(a1, 0) == 0
    assert UNISOCKS.tokenOfOwnerByIndex(a2, 0) == 1
    # Fails if index is greater than balance
    assert_fail(lambda: UNISOCKS.tokenByIndex(a1, 1))
    assert UNISOCKS.tokenByIndex(0) == 0
    assert UNISOCKS.tokenByIndex(1) == 1
    assert_fail(lambda: UNISOCKS.tokenByIndex(2))
    # Fails if not enough SOCKS are burned
    assert_fail(lambda: UNISOCKS.mint(a1, transact={}))
    # Test transfer by owner
    # UNISOCKS.transfer(a2, transact={'from': a1})
