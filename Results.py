import random
import time

class Transaction:
    def __init__(self, tx_id, amount):
        self.tx_id = tx_id
        self.amount = amount
        self.timestamp = int(time.time())  # Unix timestamp
        self.cpu_usage = random.randint(10, 20)  # Example CPU usage
        self.memory_usage = random.randint(50, 60)  # Example memory usage (MB)
        self.verification_time = random.randint(4, 5)  # Example verification time (ms)
        self.encryption_time = random.randint(3, 4)  # Example encryption time (ms)
        self.decryption_time = random.randint(2, 3)  # Example decryption time (ms)


class Block:
    def __init__(self, block_number, transactions):
        self.block_number = block_number
        self.transactions = transactions
        self.block_size = len(transactions) * 2 + 60  # Example block size calculation (KB)
        self.dynamic_accumulator_size = 0.5  # Example dynamic accumulator size (KB)
        self.total_storage = self.block_size + self.dynamic_accumulator_size  # Example total storage (KB)
        
    def transactions_per_block(self):
        return len(self.transactions)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
    def add_block(self, block):
        self.chain.append(block)
        
    def validate_chain(self):
        # Simplified validation, returning True in this example
        return True
        
    def average_block_size(self):
        return sum(block.block_size for block in self.chain) / len(self.chain) if self.chain else 0
    
    def average_total_storage(self):
        return sum(block.total_storage for block in self.chain) / len(self.chain) if self.chain else 0


def simulate_test_scenario():
    # Simulate a test scenario and return results related to transaction throughput, node count, query time, etc.
    test_cases = []
    for i in range(1, 6):
        test_case_id = f"TC00{i}"
        transaction_throughput = 500 * i
        node_count = 100 * i
        query_time = 150 + (i - 1) * 10
        block_size = 20 + (i - 1) * 2
        cross_domain_transactions = 50 * i
        test_cases.append({
            "test_case_id": test_case_id,
            "transaction_throughput": transaction_throughput,
            "node_count": node_count,
            "query_time": query_time,
            "block_size": block_size,
            "cross_domain_transactions": cross_domain_transactions
        })
    return test_cases


def main():
    blockchain = Blockchain()
    
    for i in range(1, 6):
        transactions = [Transaction(f"TX00{i}", random.randint(1, 10)) for _ in range(random.randint(20, 30))]
        block = Block(i, transactions)
        blockchain.add_block(block)
        
    test_cases = simulate_test_scenario()
    
    return blockchain, test_cases


# Run the main function
blockchain, test_cases = main()

# Extract information for the resultant tables
blockchain_info = []
for block in blockchain.chain:
    block_info = {
        "Block Number": block.block_number,
        "Block Size (KB)": block.block_size,
        "Transactions Per Block": block.transactions_per_block(),
        "Dynamic Accumulator Size (KB)": block.dynamic_accumulator_size,
        "Total Storage (MB)": block.total_storage / 1024  # Convert KB to MB for representation
    }
    blockchain_info.append(block_info)

transaction_info = []
for block in blockchain.chain:
    for tx in block.transactions:
        tx_info = {
            "Transaction ID": tx.tx_id,
            "CPU Usage (%)": tx.cpu_usage,
            "Memory Usage (MB)": tx.memory_usage,
            "Verification Time (ms)": tx.verification_time,
            "Encryption Time (ms)": tx.encryption_time,
            "Decryption Time (ms)": tx.decryption_time
        }
        transaction_info.append(tx_info)

average_block_size = blockchain.average_block_size()
average_total_storage = blockchain.average_total_storage() / 1024  # Convert KB to MB for representation

blockchain_info, transaction_info, test_cases, average_block_size, average_total_storage
