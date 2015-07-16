# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application

class StgkStarterApp(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """
    
    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        # first, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        app_payload = self.import_module("app")

        # set up a metaschema cache for global use
        self.metaschema = app_payload.CachedShotgunSchema()

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # now register the command with the engine
        self._unique_panel_id = self.engine.register_panel(self.create_panel)
        
        # register a menu entry
        self.engine.register_command("Info Panel...", self.create_panel, {"type": "panel"})
        
        
    def destroy_app(self):
        
        self.log_debug("Destroying app...")
        self.metaschema.destroy()


    def create_panel(self):
        """
        Shows the main dialog window.
        """
        app_payload = self.import_module("app")
        
        # start the UI
        try:
            return self.engine.show_panel(self._unique_panel_id, "Shotgun", self, app_payload.AppDialog)
        except AttributeError, e:
            # just to gracefully handle older engines and older cores
            self.log_warning("Could not execute show_panel method - please upgrade "
                                     "to latest core and engine! Falling back on show_dialog. Error: %s" % e)
            return self.engine.show_dialog("Shotgun", self, app_payload.AppDialog)



