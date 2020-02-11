# Cryptonote Address Validator (Python)

Simple library to validate any cryptonote based public address.

## Usage

```
from cryptonote.address import validate

# Since this tool is generic, you must provide the prefixes for the coin
# in the format [ regular, integrated, subaddress ]

prefixes = [18, 19, 42]

addresses = [
  '42ZsDR9epg1bGqCXdWGPYC5zuBmn6WGTc15nSc9sUDP8267NDTwkgk1Vn4XueSiBSjRZqaYH4PqkaLEBkGwWxrse17KHALo',
  '4CGYEDy9RwXbGqCXdWGPYC5zuBmn6WGTc15nSc9sUDP8267NDTwkgk1Vn4XueSiBSjRZqaYH4PqkaLEBkGwWxrse113DUyZY2dc1yWxsbj',
  '85CH9LW9QMXfcJTWU6hvioHC3xkLSYUFdHD7npAkoikAZDR4yKQ6wb1DA76NripyVTDm8gZSeMdKXie2BhdU95p77GKGjPZ',
]

for address in addresses:
    result = validate(address, prefixes)
    print(result)

# Outputs:
{
  valid: True,
  type: 'regular',
  prefix: '12',
  spend: '18e9cf97ada7bacce791f7f0fde2d11de1f98399629a1b007e3a5b7050954b06',
  view: '815ca9f5b39612ac0bc13d8ded455492df1acf6086cd7f72f3e4c54941c1c500',
  pid: None,
  checksum: 'f70f8a20'
}
{
  valid: True,
  type: 'integrated',
  prefix: '13',
  spend: '18e9cf97ada7bacce791f7f0fde2d11de1f98399629a1b007e3a5b7050954b06',
  view: '815ca9f5b39612ac0bc13d8ded455492df1acf6086cd7f72f3e4c54941c1c500',
  pid: '0102030405060708',
  checksum: 'a309ad4e'
}
{
  valid: True,
  type: 'sub',
  prefix: '2a',
  spend: '485a4a1b69c2d2e6d3724c0fff3e9c60cc00c5970d60a460e822214dfbc84bc0',
  view: '9860e971aeaf4448ae8e1aaf34069a4c4adeca3b7878d2f8f06440edf405ac37',
  pid: None,
  checksum: '85940a5c'
}
```

### Errors

If the address cannot be validated, it will return and object with the `valid` property set to false. You can optionally use the format `validate(address, prefixes, true)` in order to have the function throw errors, just make sure to catch them.
