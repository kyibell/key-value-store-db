import os
from LinkedList import LinkedList
import logging

logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def load_from_disk():
    '''
        Reconstructs the in-memory linked list by replaying the data.db log file.
        Each line in data.db is expected to be in "key,value" format. Lines that
        do not conform (missing the comma separator or extra/missing fields) are
        skipped with a warning so a single corrupt entry doesn't prevent startup.

        persist=False is passed to LinkedList.set() during replay to avoid
        re-writing entries that are already persisted on disk.

        Returns:
            LinkedList: The fully populated key-value store ready for use.

        Raises:
            Exception: If data.db exists but cannot be opened for reading.
    '''
    try:
        key_vals = LinkedList()

        # Check if the path exists before reading lines into the key_vals LinkedList
        if os.path.exists('data.db'):
                with open('data.db', 'r') as f:
                        for line in f:
                                line = line.strip()
                                if line:
                                        parts = line.split(',', 1)
                                        if len(parts) != 2:
                                                logger.warning(f"Skipping malformed line in data.db: {repr(line)}")
                                                continue
                                        key, value = parts
                                        key_vals.set(key, value, persist=False)
        logger.info("Successfully loaded from disk in data.db.")
        return key_vals
    
    except OSError as e:
         logger.error(f'Error opening data.db for load_from_disk(): {e}')
         raise 
        
             

def main():
    '''
        Entry point for the key-value store CLI.
        Restores any previously persisted data via load_from_disk(), then enters
        an interactive read-eval loop that accepts three commands from stdin:

            SET <key> <value>  — Store or overwrite the value for the given key.
            GET <key>          — Print the value for the given key (no output if missing).
            EXIT               — Flush any pending output and terminate the process.

        Returns:
            int: Exit code 0 on clean shutdown.
    '''
    try:
        key_vals = load_from_disk()

    except OSError:
        logger.critical(f"Failed to load from disk. Exiting...")
        return 1
    
    while True:
        try:
            user_input = input().strip()
        except EOFError:
            logger.info('EOF Recieved, Exiting...')
            break
        except KeyboardInterrupt:
            logger.info('Keyboard Interruot recieved. Exiting...')
            break
            
        if not user_input:
            # Skip blank lines instead of crashing
            continue

        parts = user_input.split(maxsplit=2)
        command = user_input.split()[0].upper()

        match command:
            case 'SET':
                try:
                # Split into at most 3 parts so values containing spaces are preserved.
                    key = parts[1]
                    value = parts[2]
                    
                    key_vals.set(key, value)
                    logger.debug(f'SET {key}, with value {value}')
                except Exception as e:
                     logger.error(f"Failed to set key: {key} and value {value}: {e}")

            case 'GET':
                key = parts[1]
                try:
                    val = key_vals.get(key)
                    # flush=True ensures the output is sent immediately
                    if val:
                        print(val, flush=True)
                except Exception as e:
                     logger.error(f'Failed to get with key {key}: {e}')
            case 'EXIT':
                # Clean exit — break out of the loop and let main() return 0.
                logger.info('EXIT command recieved. Exiting...')
                break

    
    return 0




if __name__ == '__main__':
    main()