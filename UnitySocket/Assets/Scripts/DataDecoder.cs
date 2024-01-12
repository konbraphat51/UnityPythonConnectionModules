using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

abstract class DataDecoder : ScriptableObject
{
    /// <summary>
    ///
    /// </summary>
    private Dictionary<Type, UnityEvent<Type>> correspondingEvent = default;

    /// <summary>
    /// Convert from data_type name to actual C# class type reference
    /// </summary>
    /// template:
    /// return new Dictionary<string, Type>(){
    ///     {"data_type_name", typeof(C#_class_type)}
    /// }
    public abstract Dictionary<string, Type> DataToType();

    //constructor
    public DataDecoder()
    {
        //get pre-defined data type
        Dictionary<string, Type> dataToType = DataToType();
    }
}
