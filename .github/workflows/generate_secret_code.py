# scripts/generate_secret_code.py
import uuid
import os

def get_hidden_secret_part():
    """
    Extracts parts of a hidden secret from various files and reconstructs it.
    This logic makes it convoluted for a learner to discover without knowing
    the specific file names, line numbers, and character offsets.
    """
    secret_parts_dir = 'secret_parts' # Directory where secret fragments are stored
    extracted_segments = []

    # --- Extraction Logic ---
    # This section contains the hardcoded knowledge of where each secret fragment is.
    # The regex '^VERIFIED_DOCKER_BUILD_SECRET$' is split and hidden as follows:
    # Part 1: '^VERIFIED_'
    # Part 2: 'DOCKER_BUILD'
    # Part 3: '_SECRET$'

    try:
        # Extract Part 1: '^VERIFIED_' from 'frag_a.txt'
        # Located on line 1 (0-indexed), characters 0 through 9 (inclusive).
        with open(os.path.join(secret_parts_dir, 'frag_a.txt'), 'r') as f:
            lines = f.readlines()
            if len(lines) > 1: # Ensure line 1 (0-indexed) exists
                # Extract substring from the second line (index 1)
                extracted_segments.append(lines[1].strip()[0:10])
            else:
                extracted_segments.append("ERR_P1") # Fallback if part is missing

        # Extract Part 2: 'DOCKER_BUILD' from 'frag_b.txt'
        # Located on line 1 (0-indexed), characters 24 through 35 (inclusive).
        with open(os.path.join(secret_parts_dir, 'frag_b.txt'), 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                # Extract substring from the second line (index 1)
                extracted_segments.append(lines[1].strip()[24:36])
            else:
                extracted_segments.append("ERR_P2")

        # Extract Part 3: '_SECRET$' from 'frag_c.txt'
        # Based on the content provided: "The final part is _SECRET$ in the middle of this line."
        # This is on line 1 (0-indexed), and the part "_SECRET$" starts at character 16 and ends at 24.
        with open(os.path.join(secret_parts_dir, 'frag_c.txt'), 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                # Extract substring from the second line (index 1)
                extracted_segments.append(lines[1].strip()[16:25])
            else:
                extracted_segments.append("ERR_P3")

    except FileNotFoundError as e:
        print(f"Error: One or more secret part files not found in '{secret_parts_dir}': {e}.")
        print("Please ensure 'frag_a.txt', 'frag_b.txt', 'frag_c.txt' exist in that directory.")
        return "SECRET_FILES_MISSING" # Return an error code for the secret part
    except IndexError as e:
        print(f"Error: Index out of range when extracting secret part: {e}.")
        print("This might mean the hidden secret parts are not at the expected line/character offsets in the files.")
        return "SECRET_EXTRACTION_ERROR" # Return an error code for the secret part
    except Exception as e:
        print(f"An unexpected error occurred during secret extraction: {e}")
        return "UNKNOWN_SECRET_ERROR" # Return an error code for the secret part

    # Reconstruct the full hidden secret part by joining the extracted segments
    hidden_secret = "".join(extracted_segments)
    return hidden_secret

def generate_secret_code():
    """
    Generates a unique base code (UUID) and combines it with the
    convolutedly hidden secret part extracted from files.
    """
    base_code = str(uuid.uuid4())
    
    # Retrieve the hidden secret part using the defined extraction logic
    github_secret_part = get_hidden_secret_part()
    
    # Combine the base unique code with the hidden secret part, separated by a hyphen
    combined_code = f"{base_code}-{github_secret_part}"

    return combined_code

if __name__ == "__main__":
    # When this script is executed, it prints the combined secret code to standard output.
    # The GitHub Actions workflow captures this output.
    print(generate_secret_code())
