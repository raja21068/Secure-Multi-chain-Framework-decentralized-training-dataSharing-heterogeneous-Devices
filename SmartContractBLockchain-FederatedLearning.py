from sklearn.linear_model import LinearRegression
import numpy as np


class Blockchain:
    def __init__(self, smart_contract):
        self.chain = [{'type': 'genesis', 'model': None}]  # Initialize blockchain with genesis block
        self.smart_contract = smart_contract
    
    def add_block(self, model, transaction=None):
        if transaction:
            result = self.smart_contract.execute_smart_contract(transaction)
            if result != "Executed":
                return result  # Return the error message from the smart contract
                
        block = {'type': 'model', 'model': model}
        self.chain.append(block)
        return "Block added"
    
    def validate_chain(self):
        # Implement logic to validate the blockchain
        # For simplicity, returning True in this example
        return True


class FederatedLearningServer:
    def __init__(self, participating_devices, smart_contract):
        self.participating_devices = participating_devices
        self.global_model = None
        self.blockchain = Blockchain(smart_contract)
    
    def decentralized_training(self):
        for device in self.participating_devices:
            local_model = device.train_local_model()
            self.blockchain.add_block(local_model)  # No transaction for local models
            
        self.global_model = self.aggregate_models([block['model'] for block in self.blockchain.chain if block['type'] == 'model'])
        
        # Example transaction for adding the global model to the blockchain
        transaction = {"from": "server", "to": "blockchain", "amount": 1}
        result = self.blockchain.add_block(self.global_model, transaction)
        if result != "Block added":
            raise ValueError(result)  # Raise error with the message from the smart contract or blockchain
        
        if not self.blockchain.validate_chain():
            raise ValueError("Invalid Blockchain")
        
        return self.global_model, self.blockchain

    def aggregate_models(self, local_models):
        avg_coef = np.mean([model.coef_ for model in local_models], axis=0)
        avg_intercept = np.mean([model.intercept_ for model in local_models])
        global_model = LinearRegression()
        global_model.coef_ = avg_coef
        global_model.intercept_ = avg_intercept
        return global_model


class Device:
    def __init__(self, id, data, computational_power):
        self.id = id
        self.data = data  # Assume data is a tuple (X, y) where X is features and y is target
        self.computational_power = computational_power
        self.global_model = None

    def train_local_model(self):
        X, y = self.data
        model = LinearRegression()
        model.fit(X, y)
        return model

    def receive_global_model(self, global_model):
        self.global_model = global_model


class SmartContract:
    def __init__(self, rules):
        self.rules = rules

    def validate_transaction(self, transaction):
        return all(key in transaction for key in ["from", "to", "amount"])

    def check_conditions(self, transaction):
        return transaction["amount"] <= self.rules["max_amount"]

    def execute_smart_contract(self, transaction):
        if self.validate_transaction(transaction):
            if self.check_conditions(transaction):
                return "Executed"
            else:
                return "Conditions not met"
        else:
            return "Invalid Transaction"


def main():
    data1 = (np.array([[1], [2], [3]]), np.array([2, 4, 6]))  # Device 1
    data2 = (np.array([[2], [3], [4]]), np.array([4, 6, 8]))  # Device 2
    device1 = Device(id=1, data=data1, computational_power=100)
    device2 = Device(id=2, data=data2, computational_power=50)
    rules = {"max_amount": 1}
    smart_contract = SmartContract(rules)
    federated_learning_server = FederatedLearningServer([device1, device2], smart_contract)
    global_model, blockchain = federated_learning_server.decentralized_training()
    return global_model, blockchain


global_model, blockchain = main()
blockchain.chain
