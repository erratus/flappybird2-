def calculate_subnet_masks(prefix_length):
    # Validate prefix length
    if prefix_length < 0 or prefix_length > 32:
        raise ValueError("Prefix length must be between 0 and 32")
    
    # Calculate subnet mask
    subnet_mask = [0, 0, 0, 0]
    for i in range(prefix_length):
        subnet_mask[i // 8] |= 1 << (7 - i % 8)
    
    return subnet_mask

def print_subnet_masks(subnet_masks):
    for mask in subnet_masks:
        print(".".join(map(str, mask)), end="\t")
        print("/" + str(sum(bin(byte).count("1") for byte in mask)))

def main():
    # Example prefix lengths
    prefix_lengths = [24, 25, 26, 27]
    
    # Calculate subnet masks
    subnet_masks = [calculate_subnet_masks(prefix_length) for prefix_length in prefix_lengths]
    
    # Print subnet masks
    print("Subnet Masks:")
    print_subnet_masks(subnet_masks)

if __name__ == "__main__":
    main()
