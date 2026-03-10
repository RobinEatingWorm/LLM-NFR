package org.dbmaintain.config;

import org.dbmaintain.util.DbMaintainException;
import org.dbmaintain.util.ReflectionUtils;

import java.util.Properties;

public class ConfigUtils {
  
  private static String getConfiguredClassName(Class<?> type, Properties configuration, String propertyName, String... implementationDiscriminatorValues) {
        String propKey = type.getName() + "." + propertyName;

        if (implementationDiscriminatorValues != null) {
            String implementationSpecificPropKey = propKey;
            for (String implementationDiscriminatorValue : implementationDiscriminatorValues) {
                implementationSpecificPropKey += '.' + implementationDiscriminatorValue;
            }
            if (configuration.containsKey(implementationSpecificPropKey)) {
                return PropertyUtils.getString(implementationSpecificPropKey, configuration);
            }
        }
    }
    
  }
