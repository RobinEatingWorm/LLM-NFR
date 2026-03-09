
package com.mojang.mojam;

import java.util.ArrayList;
import org.lwjgl.input.Controller;
import org.lwjgl.input.Controllers;

import com.mojang.mojam.Keys.Key;
import com.mojang.mojam.gui.AJoyBindingsMenu;
import com.mojang.mojam.gui.JoyBindingsMenu;

public class JoypadHandler {
    public Controller controller;
    public ArrayList<Object> butaxes;
    
    public int buttonCount;
    public int axisCount;
    
    public JoypadHandler(int index) {
      controller = Controllers.getController(index);

      buttonCount = controller.getButtonCount();

      axisCount = controller.getAxisCount();

      // ...

      }

}
