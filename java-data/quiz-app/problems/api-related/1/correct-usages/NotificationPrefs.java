package com.developervishalsehgal.udacityscholarsapp.data.models;

import com.google.firebase.database.Exclude;
import com.google.firebase.database.IgnoreExtraProperties;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class NotificationPrefs {

    private Boolean mCommentNotifs;
    
    public Boolean getCommentNotifs() {
         return mCommentNotifs;	         
     }	
}
    
    
    
