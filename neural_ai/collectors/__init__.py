"""
Collectors package for Neural AI Next.

This package contains data collection components for various data sources.
"""

from neural_ai.core.base.factory import Factory


class CollectorFactory(Factory):
    """Factory for creating collector instances."""
    
    def __init__(self):
        """Initialize the CollectorFactory."""
        super().__init__()
        self._implementations = {}
    
    def register_collector(self, name: str, collector_class):
        """
        Register a collector implementation.
        
        Args:
            name: Name of the collector
            collector_class: Collector class to register
        """
        self.register(name, collector_class)
    
    def get_collector(self, name: str, *args, **kwargs):
        """
        Create a collector instance.
        
        Args:
            name: Name of the collector to create
            *args: Positional arguments for the collector
            **kwargs: Keyword arguments for the collector
            
        Returns:
            Collector instance
        """
        return self.create(name, *args, **kwargs)