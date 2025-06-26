import os
import sys
import importlib.util
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class ModuleManager:
    """Manages AI modules loading and execution"""
    
    def __init__(self):
        self.modules_dir = Path("moduls")
        self.loaded_modules = {}
        self.module_configs = {}
        
        # Ensure modules directory exists
        self.modules_dir.mkdir(exist_ok=True)
        
        # Load all available modules at startup
        self.refresh_modules()
    
    def refresh_modules(self):
        """Refresh the list of available modules"""
        self.loaded_modules.clear()
        self.module_configs.clear()
        
        # Scan modules directory, excluding base_module.py
        for module_file in self.modules_dir.glob("*_module.py"):
            # Skip base_module.py as it's not a concrete AI module
            if module_file.name == "base_module.py":
                continue
            try:
                self._load_module_config(module_file)
            except Exception as e:
                print(f"Error loading module {module_file}: {e}")
    
    def _load_module_config(self, module_file: Path):
        """Load module configuration and basic info"""
        module_name = module_file.stem
        
        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module spec for {module_file}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get module class
        if not hasattr(module, 'AIModule'):
            raise AttributeError(f"Module {module_name} must have AIModule class")
        
        # Store module info
        module_class = getattr(module, 'AIModule')
        self.module_configs[module_name] = {
            'name': getattr(module_class, 'name', module_name),
            'version': getattr(module_class, 'version', '1.0.0'),
            'description': getattr(module_class, 'description', 'AI Module'),
            'file_path': module_file,
            'class': module_class
        }
    
    def get_available_modules(self) -> List[Dict[str, Any]]:
        """Get list of available modules"""
        return [
            {
                'name': config['name'],
                'version': config['version'],
                'description': config['description']
            }
            for config in self.module_configs.values()
        ]
    
    def load_module(self, module_name: str) -> bool:
        """Load a specific module for use"""
        # Find module by name
        target_config = None
        for config in self.module_configs.values():
            if config['name'] == module_name:
                target_config = config
                break
        
        if not target_config:
            return False
        
        try:
            # Initialize module instance
            module_instance = target_config['class']()
            self.loaded_modules[module_name] = module_instance
            return True
        except Exception as e:
            print(f"Error initializing module {module_name}: {e}")
            return False
    
    def get_response(self, module_name: str, user_input: str, chat_history: List[Dict]) -> str:
        """Get response from specified module"""
        if module_name not in self.loaded_modules:
            if not self.load_module(module_name):
                return "Chyba: Nelze načíst AI modul"
        
        try:
            module_instance = self.loaded_modules[module_name]
            return module_instance.generate_response(user_input, chat_history)
        except Exception as e:
            return f"Chyba při generování odpovědi: {str(e)}"
    
    def get_module_info(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific module"""
        for config in self.module_configs.values():
            if config['name'] == module_name:
                return {
                    'name': config['name'],
                    'version': config['version'],
                    'description': config['description']
                }
        return None
    
    def get_module_stats(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific module"""
        if module_name not in self.loaded_modules:
            if not self.load_module(module_name):
                return None
        
        try:
            module_instance = self.loaded_modules[module_name]
            if hasattr(module_instance, 'get_stats'):
                return module_instance.get_stats()
        except Exception as e:
            print(f"Error getting stats for {module_name}: {e}")
        
        return None
