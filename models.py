from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class Fruit:
    """
    Represents a fruit in the storage system.
    """
    id: Optional[int] = None
    name: str = ""
    quantity: int = 0
    price: float = 0.0
    storage_location: str = ""
    expiry_date: Optional[str] = None
    added_date: Optional[str] = None
    
    @property
    def total_value(self) -> float:
        """Calculate the total value of this fruit inventory."""
        return self.quantity * self.price
    
    @property
    def is_expiring_soon(self) -> bool:
        """Check if the fruit is expiring within 7 days."""
        if not self.expiry_date:
            return False
        
        from datetime import datetime, timedelta
        expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        today = datetime.now().date()
        return (expiry - today).days <= 7 and (expiry - today).days >= 0
    
    @property
    def is_expired(self) -> bool:
        """Check if the fruit has already expired."""
        if not self.expiry_date:
            return False
        
        from datetime import datetime
        expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        today = datetime.now().date()
        return expiry < today
    
    def to_tuple(self) -> tuple:
        """Convert the fruit object to a tuple for database operations."""
        return (self.name, self.quantity, self.price, self.storage_location, self.expiry_date)
    
    @classmethod
    def from_tuple(cls, data_tuple):
        """Create a Fruit object from a database tuple."""
        return cls(
            id=data_tuple[0],
            name=data_tuple[1],
            quantity=data_tuple[2],
            price=data_tuple[3],
            storage_location=data_tuple[4],
            expiry_date=data_tuple[5],
            added_date=data_tuple[6]
        )


@dataclass
class Category:
    """
    Represents a category for fruits.
    """
    id: Optional[int] = None
    name: str = ""
    
    def to_tuple(self) -> tuple:
        """Convert the category object to a tuple for database operations."""
        return (self.name,)


@dataclass
class FruitInventory:
    """
    Represents the entire fruit inventory.
    """
    fruits: List[Fruit] = None
    
    def __post_init__(self):
        if self.fruits is None:
            self.fruits = []
    
    @property
    def total_inventory_value(self) -> float:
        """Calculate the total value of the entire inventory."""
        return sum(fruit.total_value for fruit in self.fruits)
    
    @property
    def expiring_soon(self) -> List[Fruit]:
        """Get a list of fruits that are expiring soon."""
        return [fruit for fruit in self.fruits if fruit.is_expiring_soon]
    
    @property
    def expired(self) -> List[Fruit]:
        """Get a list of fruits that have already expired."""
        return [fruit for fruit in self.fruits if fruit.is_expired]
    
    def add_fruit(self, fruit: Fruit) -> None:
        """Add a fruit to the inventory."""
        self.fruits.append(fruit)
    
    def remove_fruit(self, fruit_id: int) -> bool:
        """Remove a fruit from the inventory by ID."""
        for i, fruit in enumerate(self.fruits):
            if fruit.id == fruit_id:
                self.fruits.pop(i)
                return True
        return False
    
    def get_fruit_by_id(self, fruit_id: int) -> Optional[Fruit]:
        """Get a fruit by its ID."""
        for fruit in self.fruits:
            if fruit.id == fruit_id:
                return fruit
        return None
    
    def update_fruit(self, updated_fruit: Fruit) -> bool:
        """Update a fruit in the inventory."""
        for i, fruit in enumerate(self.fruits):
            if fruit.id == updated_fruit.id:
                self.fruits[i] = updated_fruit
                return True
        return False