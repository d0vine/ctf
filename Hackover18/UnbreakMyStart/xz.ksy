meta:
  id: xz
  endian: le
seq:
  - id: header
    type: header
types:
  header:
    seq:
      - id: magic
        contents: [0xfd, 7zXZ, 0x00]
