
package org.cocos2d.nodes;

import org.cocos2d.opengl.CCTexture2D;
import org.cocos2d.opengl.GLResourceHelper;
import org.cocos2d.protocols.CCLabelProtocol;
import org.cocos2d.types.CGRect;
import org.cocos2d.types.CGSize;

public class CCLabel extends CCSprite implements CCLabelProtocol {
    
    texture.setLoader(new GLResourceHelper.GLResourceLoader() {
    		@Override
    		public void load(GLResourceHelper.Resource res) {
    	    	if (CGSize.equalToSize(_dimensions, CGSize.zero())) {
    	    		((CCTexture2D)res).initWithText(string, _fontName, _fontSize);
    	    	} else {
    	    		((CCTexture2D)res).initWithText(string, _dimensions, _alignment, _fontName, _fontSize);
    	    	}
    		    CGSize size = texture_.getContentSize();
    		    setTextureRect(CGRect.make(0, 0, size.width, size.height));
    		}
    	});

}
