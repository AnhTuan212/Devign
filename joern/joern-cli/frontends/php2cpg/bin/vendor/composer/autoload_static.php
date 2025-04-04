<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInitf1f3728acb4006603e0fe71a85c1e586
{
    public static $prefixLengthsPsr4 = array (
        'P' => 
        array (
            'PhpParser\\' => 10,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'PhpParser\\' => 
        array (
            0 => __DIR__ . '/..' . '/nikic/php-parser/lib/PhpParser',
        ),
    );

    public static $classMap = array (
        'Composer\\InstalledVersions' => __DIR__ . '/..' . '/composer/InstalledVersions.php',
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInitf1f3728acb4006603e0fe71a85c1e586::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInitf1f3728acb4006603e0fe71a85c1e586::$prefixDirsPsr4;
            $loader->classMap = ComposerStaticInitf1f3728acb4006603e0fe71a85c1e586::$classMap;

        }, null, ClassLoader::class);
    }
}
