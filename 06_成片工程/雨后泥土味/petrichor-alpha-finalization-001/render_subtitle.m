#import <AppKit/AppKit.h>

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        if (argc < 3) return 2;
        [NSApplication sharedApplication];
        NSString *output = [NSString stringWithUTF8String:argv[1]];
        NSMutableArray<NSString *> *lines = [NSMutableArray array];
        for (int index = 2; index < argc && index < 4; index++) {
            [lines addObject:[NSString stringWithUTF8String:argv[index]]];
        }
        NSBitmapImageRep *bitmap = [[NSBitmapImageRep alloc]
            initWithBitmapDataPlanes:NULL pixelsWide:720 pixelsHigh:1280 bitsPerSample:8
            samplesPerPixel:4 hasAlpha:YES isPlanar:NO colorSpaceName:NSDeviceRGBColorSpace
            bitmapFormat:0 bytesPerRow:0 bitsPerPixel:0];
        if (!bitmap) return 3;
        [NSGraphicsContext saveGraphicsState];
        NSGraphicsContext *context = [NSGraphicsContext graphicsContextWithBitmapImageRep:bitmap];
        [NSGraphicsContext setCurrentContext:context];
        [[NSColor clearColor] setFill];
        NSRectFillUsingOperation(NSMakeRect(0, 0, 720, 1280), NSCompositingOperationCopy);

        NSBezierPath *panel = [NSBezierPath bezierPathWithRoundedRect:NSMakeRect(38, 85, 644, 140) xRadius:18 yRadius:18];
        [[NSColor colorWithCalibratedRed:0.063 green:0.078 blue:0.075 alpha:0.54] setFill];
        [panel fill];

        NSMutableParagraphStyle *paragraph = [[NSMutableParagraphStyle alloc] init];
        paragraph.alignment = NSTextAlignmentCenter;
        NSFont *font = [NSFont fontWithName:@"PingFangSC-Medium" size:38] ?: [NSFont systemFontOfSize:38 weight:NSFontWeightMedium];
        NSDictionary *attributes = @{
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: [NSColor colorWithCalibratedWhite:0.95 alpha:1.0],
            NSStrokeColorAttributeName: [NSColor colorWithCalibratedRed:0.067 green:0.082 blue:0.078 alpha:0.9],
            NSStrokeWidthAttributeName: @(-2.0),
            NSParagraphStyleAttributeName: paragraph
        };
        CGFloat baseY = lines.count == 2 ? 151 : 126;
        for (NSUInteger index = 0; index < lines.count; index++) {
            [lines[index] drawInRect:NSMakeRect(52, baseY - index * 52, 616, 48) withAttributes:attributes];
        }
        [context flushGraphics];
        [NSGraphicsContext restoreGraphicsState];
        NSData *png = [bitmap representationUsingType:NSBitmapImageFileTypePNG properties:@{}];
        if (!png) return 4;
        return [png writeToFile:output atomically:YES] ? 0 : 5;
    }
}
